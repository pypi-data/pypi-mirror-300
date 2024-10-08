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

import logging

from azure.core.exceptions import ResourceNotFoundError
from azure.mgmt.compute.models import VirtualMachine

from clusterondemand.clusternameprefix import clusterprefix_ns, ensure_cod_prefix
from clusterondemand.utils import confirm, confirm_ns, log_no_clusters_found, multithread_run
from clusterondemandazure.base import ClusterCommand
from clusterondemandazure.clusterlist import (
    get_cod_resource_groups,
    get_head_a_names,
    get_head_b_names,
    name_from_r_group
)
from clusterondemandconfig import ConfigNamespace, config

from .configuration import azurecommon_ns

log = logging.getLogger("cluster-on-demand")


HR = "---------------------------------------------------------------------"

config_ns = ConfigNamespace("azure.cluster.delete", "cluster delete parameter")
config_ns.import_namespace(azurecommon_ns)
config_ns.import_namespace(clusterprefix_ns)
config_ns.import_namespace(confirm_ns)
config_ns.add_repeating_positional_parameter(
    "filters",
    help="Cluster names or patterns. Wildcards are supported (e.g: \\*)",
)
config_ns.add_parameter(
    "resource_group",
    help="Name of resource group to delete. Only the resources created by COD will be deleted."
)
config_ns.add_switch_parameter(
    "partial",
    help="Perform a partial removal which removes everything within the resource group except for "
         "the storage account and the images stored within (both head node and node-installer images)"
         " but not the resource group itself."
         "This enables creating clusters more quickly by reusing existing resource groups."
)
config_ns.add_switch_parameter(
    "dry_run",
    help="Do not actually delete the resources."
)


def run_command():
    ClusterDelete().run()


class ClusterDelete(ClusterCommand):

    def delete_virtual_machines(self, resource_group_name):
        cluster_name = name_from_r_group(resource_group_name)
        head_node_names = get_head_a_names(cluster_name) + get_head_b_names(cluster_name)
        removal_ops = []
        for entity in self.azure_api.compute_client.virtual_machines.list(resource_group_name):
            if entity.tags and entity.tags.get("BCM Resource", False):
                if entity.name in head_node_names:
                    self.delete_role_assignments(entity, resource_group_name)
                log.info(f"Deleting virtual machine {entity.name}")
                if not config["dry_run"]:
                    async_removal = self.azure_api.compute_client.virtual_machines.begin_delete(resource_group_name,
                                                                                                entity.name)
                    removal_ops.append(async_removal)

        for removal in removal_ops:
            removal.wait()

    def delete_role_assignments(self, vm: VirtualMachine, resource_group_name: str):
        if not (vm.identity and vm.identity.type == "SystemAssigned" and vm.identity.principal_id is not None):
            return
        auth_client = self.azure_api.authorization_management_client
        for role_assignment in auth_client.role_assignments.list_for_resource_group(
                resource_group_name=resource_group_name, filter=f"principalid eq '{vm.identity.principal_id}'"):
            log.info(f"Deleting role assignment {role_assignment.name} of virtual machine {vm.name}")
            if not config["dry_run"]:
                auth_client.role_assignments.delete(role_assignment.scope, role_assignment.name)

    def delete_network_interfaces(self, resource_group_name):
        removal_ops = []
        for entity in self.azure_api.network_client.network_interfaces.list(resource_group_name):
            if entity.tags and entity.tags.get("BCM Resource", False):
                log.info(f"Deleting network interface {entity.name}")
                if not config["dry_run"]:
                    async_removal = self.azure_api.network_client.network_interfaces.begin_delete(resource_group_name,
                                                                                                  entity.name)
                    removal_ops.append(async_removal)
        for removal in removal_ops:
            removal.wait()

    def delete_private_endpoints(self, resource_group_name):
        removal_ops = []
        for entity in self.azure_api.network_client.private_endpoints.list(resource_group_name):
            if entity.tags and entity.tags.get("BCM Resource", False):
                log.info(f"Deleting private endpoint {entity.name}")
                if not config["dry_run"]:
                    async_removal = self.azure_api.network_client.private_endpoints.begin_delete(resource_group_name,
                                                                                                 entity.name)
                    removal_ops.append(async_removal)
        for removal in removal_ops:
            removal.wait()

    def delete_virtual_networks(self, resource_group_name):
        removal_ops = []
        for entity in self.azure_api.network_client.virtual_networks.list(resource_group_name):
            if entity.tags and entity.tags.get("BCM Resource", False):
                log.info(f"Deleting virtual network {entity.name}")
                if not config["dry_run"]:
                    async_removal = self.azure_api.network_client.virtual_networks.begin_delete(resource_group_name,
                                                                                                entity.name)
                    removal_ops.append(async_removal)
        for removal in removal_ops:
            removal.wait()

    def delete_public_ips(self, resource_group_name):
        removal_ops = []
        for entity in self.azure_api.network_client.public_ip_addresses.list(resource_group_name):
            if entity.tags and entity.tags.get("BCM Resource", False):
                log.info(f"Deleting public ip address {entity.name}")
                if not config["dry_run"]:
                    async_removal = self.azure_api.network_client.public_ip_addresses.begin_delete(resource_group_name,
                                                                                                   entity.name)
                    removal_ops.append(async_removal)
        for removal in removal_ops:
            removal.wait()

    def delete_security_groups(self, resource_group_name):
        removal_ops = []
        for entity in self.azure_api.network_client.network_security_groups.list(resource_group_name):
            if entity.tags and entity.tags.get("BCM Resource", False):
                log.info(f"Deleting network security group {entity.name}")
                if not config["dry_run"]:
                    async_removal = self.azure_api.network_client.network_security_groups.begin_delete(
                        resource_group_name, entity.name)
                    removal_ops.append(async_removal)
        for removal in removal_ops:
            removal.wait()

    def delete_availability_sets(self, resource_group_name):
        for entity in self.azure_api.compute_client.availability_sets.list(resource_group_name):
            if entity.tags and entity.tags.get("BCM Resource", False):
                log.info(f"Deleting availability set {entity.name}")
                if not config["dry_run"]:
                    self.azure_api.compute_client.availability_sets.delete(
                        resource_group_name, entity.name)

    def delete_disks(self, resource_group_name):
        removal_ops = []
        for entity in self.azure_api.compute_client.disks.list_by_resource_group(resource_group_name):
            if entity.tags and entity.tags.get("BCM Resource", False):
                log.info(f"Deleting disk {entity.name}")
                if not config["dry_run"]:
                    async_removal = self.azure_api.compute_client.disks.begin_delete(resource_group_name, entity.name)
                    removal_ops.append(async_removal)
        for removal in removal_ops:
            removal.wait()

    def delete_snapshots(self, resource_group_name):
        removal_ops = []
        for entity in self.azure_api.compute_client.snapshots.list_by_resource_group(resource_group_name):
            if entity.tags and entity.tags.get("BCM Resource", False):
                log.info(f"Deleting snapshot {entity.name}")
                if not config["dry_run"]:
                    async_removal = self.azure_api.compute_client.snapshots.begin_delete(resource_group_name,
                                                                                         entity.name)
                    removal_ops.append(async_removal)
        for removal in removal_ops:
            removal.wait()

    def delete_storage_accounts(self, resource_group_name):
        for entity in self.azure_api.storage_client.storage_accounts.list_by_resource_group(resource_group_name):
            if entity.tags and entity.tags.get("BCM Resource", False):
                log.info(f"Deleting storage account {entity.name}")
                if not config["dry_run"]:
                    self.azure_api.storage_client.storage_accounts.delete(resource_group_name, entity.name)

    def delete_images(self, resource_group_name):
        removal_ops = []
        for entity in self.azure_api.compute_client.images.list_by_resource_group(resource_group_name):
            if entity.tags and entity.tags.get("BCM Resource", False):
                log.info(f"Deleting image {entity.name}")
                if not config["dry_run"]:
                    async_removal = self.azure_api.compute_client.images.begin_delete(resource_group_name, entity.name)
                    removal_ops.append(async_removal)
        for removal in removal_ops:
            removal.wait()

    def delete_resources(self, resource_group):
        resource_group_name = resource_group.name

        # For clusters older than 9.0, cmaemon doesn't tag the VMs. So they don't get deleted and
        # delete_virtual_networks fails. So, if the RG is going to get deleted, let's do the
        # whole thing at once so the deletion will work in any cluster
        if not config["partial"] and resource_group.tags and resource_group.tags.get("BCM Resource", False):
            log.info(f"Deleting resource group {resource_group_name}")
            if not config["dry_run"]:
                async_removal = self.azure_api.resource_client.resource_groups.begin_delete(resource_group_name)
                async_removal.wait()
        else:
            log.info(f"Deleting resources in resource group {resource_group_name}")

            self.delete_virtual_machines(resource_group_name)
            self.delete_private_endpoints(resource_group_name)
            self.delete_network_interfaces(resource_group_name)
            self.delete_virtual_networks(resource_group_name)
            self.delete_public_ips(resource_group_name)
            self.delete_security_groups(resource_group_name)
            self.delete_disks(resource_group_name)
            self.delete_snapshots(resource_group_name)
            self.delete_availability_sets(resource_group_name)

            if not config["partial"]:
                self.delete_images(resource_group_name)
                self.delete_storage_accounts(resource_group_name)

        log.info("Resources deleted successfully")

    def run(self):
        self._validate_params()

        if config["filters"] and not config["resource_group"]:
            names = [ensure_cod_prefix(name) for name in config["filters"]]
            cod_resource_groups = get_cod_resource_groups(self.azure_api.resource_client, names)
        elif config["resource_group"] and not config["filters"]:
            try:
                cod_resource_groups = [self.azure_api.resource_client.resource_groups.get(config["resource_group"])]
            except ResourceNotFoundError as e:
                log.error(f"Code: {e.error.code}, {e.error.message}")
                return
        else:
            log.error("Need to specify either cluster name, or resource group name of clusters to be deleted")
            return
        rg_names = [rg.name for rg in cod_resource_groups]

        if not cod_resource_groups:
            log_no_clusters_found("delete")
            return

        if config["dry_run"]:
            log.warning("Running in dry run mode. The resources will not be deleted.")

        if not confirm(f"This will delete resource groups {' '.join(rg_names)}, continue?"):
            return

        multithread_run(self.delete_resources, cod_resource_groups, config["max_threads"])

    def _validate_params(self):
        self._validate_access_credentials()
