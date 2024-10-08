# Copyright 2004-2024 Bright Computing Holding BV
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import annotations

import fnmatch
import logging
import re
from dataclasses import dataclass

from azure.core.exceptions import HttpResponseError, ResourceNotFoundError
from azure.mgmt.compute.models import VirtualMachine

import clusterondemand.clustercreate
from clusterondemand.clusternameprefix import clusterprefix_ns, ensure_cod_prefix
from clusterondemand.codoutput.sortingutils import ClusterIPs, SortableData
from clusterondemand.exceptions import UserReportableException
from clusterondemand.utils import log_no_clusters_found
from clusterondemandazure.azure_actions.credentials import AzureApiHelper
from clusterondemandazure.base import ClusterCommand
from clusterondemandconfig import ConfigNamespace, config

from .configuration import azurecommon_ns

log = logging.getLogger("cluster-on-demand")

ALL_COLUMNS = [
    ("cluster_name", "Cluster Name"),
    ("head_node_name", "Head Node Name"),
    ("ip", "IP"),
    ("location", "Location"),
    ("resource_group_name", "Resource group"),
    ("head_node_vmsize", "Head Node VM Size"),
    ("head_node_cpu", "Head Node CPU Cores"),
    ("head_node_ram", "Head Node RAM (MB)"),
    ("created", "Image Created"),
    ("image_name", "Image Name"),
]

DEFAULT_COLUMNS = [
    "cluster_name",
    "head_node_name",
    "ip",
    "location",
    "head_node_vmsize",
    "head_node_cpu",
    "head_node_ram",
    "created",
    "image_name",
]

_COD_RESOURCE_GROUP_SUFFIX = "_cod_resource_group"
_HA_NODE_A_SUFFIX = "-a"
_HA_NODE_B_SUFFIX = "-b"
_HA_IP_SUFFIX = "-shared-ip"

config_ns = ConfigNamespace("azure.cluster.list", help_section="list output parameters")
config_ns.import_namespace(clusterondemand.configuration.clusterlist_ns)
config_ns.import_namespace(clusterprefix_ns)
config_ns.import_namespace(azurecommon_ns)
config_ns.add_enumeration_parameter(
    "sort",
    choices=[column[0] for column in ALL_COLUMNS],
    default=["created"],
    help="Sort results by one (or two) of the columns",
)
config_ns.add_enumeration_parameter(
    "columns",
    choices=[column[0] for column in ALL_COLUMNS],
    default=DEFAULT_COLUMNS,
    help="Provide space separated set of columns to be displayed",
)
config_ns.add_repeating_positional_parameter(
    "filters",
    default=["*"],
    require_value=True,
    help="Cluster names or patterns to be listed. Default: all clusters. Wildcards are supported (e.g: \\*)",
)


def run_command():
    ClusterList().run()


class ClusterList(ClusterCommand):

    def run(self):
        try:
            self._validate_params()
        except HttpResponseError as e:
            if "SubscriptionNotFound" in e.error.code:
                raise UserReportableException(str(e))
            AzureApiHelper.log_error_details(e)
            raise e

        rows = []
        global_vmsizes = {}
        names = [ensure_cod_prefix(name) for name in config["filters"]]
        cod_resource_groups = get_cod_resource_groups(self.azure_api.resource_client, names)

        if not cod_resource_groups:
            log_no_clusters_found("list")
            return

        for r_group in cod_resource_groups:
            rows.append(get_cluster_data(self.azure_api, r_group, global_vmsizes))

        cols_id = config["columns"]
        if not cols_id:
            cols_id = DEFAULT_COLUMNS

        table = SortableData(all_headers=ALL_COLUMNS, requested_headers=cols_id, rows=rows)
        table.sort(*config["sort"])

        print(table.output(output_format=config["output_format"]))

    def _validate_params(self):
        self._validate_access_credentials()


@dataclass(frozen=True)
class NodeInfo:
    name: str
    vm: VirtualMachine
    vm_size: str
    cpu_cores: int
    ram_in_mb: int
    image_creation_date: str | None
    image_name: str | None


def _get_node_info(azure_api, r_group, names: list[str], global_vmsizes) -> NodeInfo | None:
    vm = None
    for name in names:
        try:
            vm = azure_api.compute_client.virtual_machines.get(r_group.name, name)
        except ResourceNotFoundError:
            pass
        if vm is not None:
            break
    if vm is None:
        log.debug("Head node VM not found")
        return None

    specs = get_location_vmsize_details(
        azure_api.compute_client,
        global_vmsizes,
        r_group.location,
        vm.hardware_profile.vm_size,
    )
    return NodeInfo(
        name=name,
        vm=vm,
        vm_size=vm.hardware_profile.vm_size,
        cpu_cores=specs["number_of_cores"],
        ram_in_mb=specs["memory_in_mb"],
        image_creation_date=vm.tags.get(
            "BCM Image created at", vm.tags.get("image_creation_date", None)
        ),
        image_name=vm.tags.get("BCM Image name", vm.tags.get("image_name", None)),
    )


def _get_vm_ips(azure_api, r_group, vm, ip_names):
    public_ip, private_ip = None, None
    for ip_name in ip_names:
        try:
            public_ip = azure_api.network_client.public_ip_addresses.get(
                r_group.name, ip_name
            ).ip_address
        except ResourceNotFoundError:
            pass
        if public_ip is not None:
            break
    if public_ip is None:
        log.debug(f"Failed getting public ip for head node: {vm.name}")

    # There are 2 reasons why Public IP might be missing:
    # 1. Azure malfunction or user error, removed public IP (bad case)
    # 2. Cluster was created without public IP, as customer has infrastructure to reach Azure cloud (E.g. on-site VPN)
    # In either case, we need to get private IP to log something for the user. But as we can't tell if we're dealing
    # with a bad case, we log warning in any case
    if not public_ip and vm:
        try:
            # cod interface and ip configuration is primary, even if user manually added interfaces
            interfaces = vm.network_profile.network_interfaces
            cod_interface = next(i for i in interfaces if i.primary)
            nic_name = " ".join(cod_interface.id.split("/")[-1:])
            private_ip = next(
                ip_conf.private_ip_address
                for ip_conf in azure_api.network_client.network_interfaces.get(
                    r_group.name, nic_name
                ).ip_configurations
                if ip_conf.primary
            )
        except Exception as e:
            log.debug(f"Failed getting head node private ip: {e}")
    return public_ip, private_ip


def get_cluster_data(azure_api, r_group, global_vmsizes):
    """
    Return list containing cluster information of a given resource group.

    :param azure_api: instance of AzureApiHelper
    :param r_group: resource group object
    :param global_vmsizes: global dictionary mapping
    :return: cluster information in the following format:
        [
            cluster_name,
            head_node_name,
            ip,
            location,
            resource_group_name,
            vm_size,
            cpu_cores,
            ram,
            image_creation_date,
            image_name,
        ]
    """
    missing_resources = []
    cluster_name = name_from_r_group(r_group.name)
    head_node_a_names = get_head_a_names(cluster_name)
    head_node_b_names = get_head_b_names(cluster_name)

    head_node_a = _get_node_info(azure_api, r_group, head_node_a_names, global_vmsizes)
    head_node_b = _get_node_info(azure_api, r_group, head_node_b_names, global_vmsizes)

    if head_node_a is not None:
        public_ip_a, private_ip_a = _get_vm_ips(
            azure_api, r_group, head_node_a.vm, [f"{head_node_a.name}-ip", "head-node-public-ip"]
        )
    else:
        public_ip_a, private_ip_a = (None, None)

    if head_node_b is not None:
        public_ip_b, private_ip_b = _get_vm_ips(
            azure_api, r_group, head_node_b.vm, [f"{head_node_b.name}-ip"]
        )
    else:
        public_ip_b, private_ip_b = (None, None)

    shared_ip = None
    try:
        shared_ip = azure_api.network_client.public_ip_addresses.get(
            r_group.name, cluster_name + _HA_IP_SUFFIX
        ).ip_address
    except Exception as e:
        log.debug(f"Failed getting public ip: {e}")

    is_ha = shared_ip is not None or head_node_b is not None

    if head_node_a is None or is_ha and head_node_b is None:
        missing_resources.append("head node")

    if public_ip_a is None or is_ha and (public_ip_b is None or shared_ip is None):
        missing_resources.append("public ip")

    head_node_a_name = (head_node_a.name if head_node_a else None) or "?"
    head_node_b_name = (head_node_b.name if head_node_b else None) or "?"
    head_node_a_vm_size = (head_node_a.vm_size if head_node_a else None) or "?"
    head_node_b_vm_size = (head_node_b.vm_size if head_node_b else None) or "?"
    head_node_a_cpu_cores = (str(head_node_a.cpu_cores) if head_node_a else None) or "?"
    head_node_b_cpu_cores = (str(head_node_b.cpu_cores) if head_node_b else None) or "?"
    head_node_a_ram_in_mb = (str(head_node_a.ram_in_mb) if head_node_a else None) or "?"
    head_node_b_ram_in_mb = (str(head_node_b.ram_in_mb) if head_node_b else None) or "?"
    head_node_a_image_creation_date = (
        head_node_a.image_creation_date if head_node_a else None
    ) or "?"
    head_node_b_image_creation_date = (
        head_node_b.image_creation_date if head_node_b else None
    ) or "?"
    head_node_a_image_name = (head_node_a.image_name if head_node_a else None) or "?"
    head_node_b_image_name = (head_node_b.image_name if head_node_b else None) or "?"

    if is_ha:
        head_node_name_col = "\n".join(
            [
                head_node_a_name + " (A)" if head_node_a is not None else "missing",
                head_node_b_name + " (B)" if head_node_b is not None else "missing",
            ]
        )
        head_node_vm_size_col = "\n".join([head_node_a_vm_size, head_node_b_vm_size])
        head_node_cpu_cores_col = "\n".join([head_node_a_cpu_cores, head_node_b_cpu_cores])
        head_node_ram_in_mb_col = "\n".join([head_node_a_ram_in_mb, head_node_b_ram_in_mb])
        head_node_image_creation_date_col = "\n".join(
            [head_node_a_image_creation_date, head_node_b_image_creation_date]
        )
        head_node_image_name_col = "\n".join([head_node_a_image_name, head_node_b_image_name])
    else:
        head_node_name_col = head_node_a_name
        head_node_vm_size_col = head_node_a_vm_size
        head_node_cpu_cores_col = head_node_a_cpu_cores
        head_node_ram_in_mb_col = head_node_a_ram_in_mb
        head_node_image_creation_date_col = head_node_a_image_creation_date
        head_node_image_name_col = head_node_a_image_name

    cluster_ips = ClusterIPs(
        primary_ip=public_ip_a,
        primary_private_ip=private_ip_a,
        secondary_ip=public_ip_b,
        secondary_private_ip=private_ip_b,
        shared_ip=shared_ip,
    )

    if missing_resources:
        log.warning(
            f"Resource(s) {', '.join(missing_resources)!r} for cluster {cluster_name} cannot be found, "
            f"this could be a sign of a broken deployment. You can remove the cluster by running: "
            f"cm-cod-azure cluster delete {cluster_name}"
        )

    return [
        cluster_name,
        head_node_name_col,
        cluster_ips,
        r_group.location,
        r_group.name,
        head_node_vm_size_col,
        head_node_cpu_cores_col,
        head_node_ram_in_mb_col,
        head_node_image_creation_date_col,
        head_node_image_name_col,
    ]


def get_location_vmsize_details(compute_client, global_vmsizes, location, vmsize_name):
    """
    Return details of virtual machine size.

    Checks if vmsize already exists in the global dictionary [global_vmsizes]
    then returns its properties
    Otherwise, pulls that vmsize's information, adds them to the global dictionary
    then returns its properties

    :param compute_client: azure sdk compute client
    :param global_vmsizes: global dictionary mapping vmsizes and their properties
    :param location: location of the given vmsize
    :param vmsize_name: name of the vmsize
    :return: a dictionary of the vmsize information in the following format :
        {
            "number_of_cores": number_of_cores,
            "memory_in_mb": memory_in_mb,
        }
    """
    if vmsize_name in global_vmsizes:
        return global_vmsizes[vmsize_name]

    paged_vmsizes = compute_client.virtual_machine_sizes.list(location=location)
    vmsize = next(paged_vmsizes)
    while vmsize:
        if vmsize.name in vmsize_name:
            global_vmsizes[vmsize_name] = {
                "number_of_cores": vmsize.number_of_cores,
                "memory_in_mb": vmsize.memory_in_mb,
            }
            return global_vmsizes[vmsize_name]
        try:
            vmsize = next(paged_vmsizes)
        except GeneratorExit:
            break


def name_from_r_group(r_group_name):
    """
    Obtain name of resource group.

    :param r_group_name: resource group name
    :return: extracted cluster name from group name
    """
    return r_group_name.removesuffix(_COD_RESOURCE_GROUP_SUFFIX)


def get_head_a_names(cluster_name: str) -> list[str]:
    return [cluster_name + _HA_NODE_A_SUFFIX, cluster_name]


def get_head_b_names(cluster_name: str) -> list[str]:
    return [cluster_name + _HA_NODE_B_SUFFIX]


def get_cod_resource_groups(resource_client, patterns):
    """
    Return COD resource groups.

    :param resource_client: azure sdk resource client
    :return: list of resource groups containing cod-azure clusters
    """

    regexes = [fnmatch.translate(f"{p}{_COD_RESOURCE_GROUP_SUFFIX}") for p in patterns]

    r_groups = [
        item
        for item in resource_client.resource_groups.list()
        if any(re.match(r, item.name) for r in regexes)
    ]
    return r_groups
