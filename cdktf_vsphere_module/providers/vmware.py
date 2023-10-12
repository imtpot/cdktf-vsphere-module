# vmware.py

from constructs import Construct
from cdktf import TerraformStack, TerraformOutput
from cdktf_cdktf_provider_vsphere.provider import VsphereProvider
from cdktf_cdktf_provider_vsphere.data_vsphere_datacenter import DataVsphereDatacenter
from cdktf_cdktf_provider_vsphere.data_vsphere_datastore import DataVsphereDatastore
from cdktf_cdktf_provider_vsphere.data_vsphere_compute_cluster import DataVsphereComputeCluster
from cdktf_cdktf_provider_vsphere.data_vsphere_network import DataVsphereNetwork
from cdktf_cdktf_provider_vsphere.data_vsphere_virtual_machine import DataVsphereVirtualMachine
from cdktf_cdktf_provider_vsphere.virtual_machine import (
    VirtualMachine, VirtualMachineNetworkInterface, VirtualMachineDisk, VirtualMachineClone
)
from ..models.dataclasses import VsphereConfig, VMConfig
from ..services.helpers import ConfigService


class VMConfigurator:
    """Handles the configuration setup for VM related resources."""

    def __init__(self, parent, vm_config: VMConfig):
        self.parent = parent
        self.vm_config = vm_config
        self._setup_resources()

    def _setup_resources(self):
        self.datacenter = DataVsphereDatacenter(self.parent, "Datacenter", name=self.vm_config.datacenter)
        self.cluster = DataVsphereComputeCluster(self.parent, "Cluster", name=self.vm_config.cluster,
                                                 datacenter_id=self.datacenter.id)
        self.datastore = DataVsphereDatastore(self.parent, "Datastore", name=self.vm_config.datastore,
                                              datacenter_id=self.datacenter.id)
        self.disks = self._configure_disks()
        self.networks = self._configure_networks()
        self.template = self._configure_template()

    def _configure_disks(self) -> list:
        """Configure the VM disks."""
        return [
            VirtualMachineDisk(
                label=disk_name,
                size=disk_size,
                unit_number=int(idx),
                thin_provisioned=True
            )
            for idx, (disk_name, disk_size) in enumerate(self.vm_config.disks.items())
        ]

    def _configure_networks(self) -> list:
        """Configure the VM networks."""
        return [
            VirtualMachineNetworkInterface(
                network_id=DataVsphereNetwork(
                    self.parent, network, name=network, datacenter_id=self.datacenter.id
                ).id
            )
            for network, _ in self.vm_config.networks.items()
        ]

    def _configure_template(self):
        """Configure the VM template."""
        return DataVsphereVirtualMachine(self.parent, "Template", name=self.vm_config.template,
                                         datacenter_id=self.datacenter.id)


class VirtualMachineConstruct(Construct):
    """Creates a Virtual Machine in VMware."""

    def __init__(self, scope: Construct, id: str, vm_config: VMConfig):
        super().__init__(scope, id)
        configurator = VMConfigurator(self, vm_config)
        self._create_vm_instance(vm_config, configurator)

    def _create_vm_instance(self, vm_config: VMConfig, configurator):
        extra_config = ConfigService.generate_extra_config(vm_config)
        vm = VirtualMachine(
            self, "VirtualMachine",
            resource_pool_id=configurator.cluster.resource_pool_id,
            datastore_id=configurator.datastore.id,
            name=vm_config.name,
            num_cpus=vm_config.num_cpus,
            memory=vm_config.memory,
            guest_id=configurator.template.guest_id,
            disk=configurator.disks,
            network_interface=configurator.networks,
            clone=VirtualMachineClone(template_uuid=configurator.template.id),
            firmware=vm_config.firmware,
            extra_config=extra_config,
            lifecycle={"ignore_changes": ["hv_mode", "ept_rvi_mode"]}
        )

        TerraformOutput(self, "vm_ip", value=vm.default_ip_address)


class VsphereProviderConstruct(Construct):
    """Configures the Vsphere Provider."""

    def __init__(self, scope: Construct, id: str, vsphere_config: VsphereConfig):
        super().__init__(scope, id)
        VsphereProvider(
            self, id,
            user=vsphere_config.user,
            password=vsphere_config.password,
            vsphere_server=vsphere_config.vsphere_server,
            allow_unverified_ssl=vsphere_config.allow_unverified_ssl
        )


class VMwareStack(TerraformStack):
    """Main stack for VMware configurations."""

    def __init__(self, scope: Construct, id: str, vsphere_config: VsphereConfig):
        super().__init__(scope, id)
        VsphereProviderConstruct(self, f"{id}_provider", vsphere_config)

    def create_vm(self, vm_config: VMConfig):
        """Create a new VM."""
        VirtualMachineConstruct(self, f"{id}_{vm_config.name}", vm_config)
