# main.py

from cdktf import App
from cdktf_vsphere_module.models.dataclasses import VsphereConfig, VMConfig, VMNetworkConfig
from cdktf_vsphere_module.providers.vmware import VMwareStack


app = App()

vm_config_1 = VMConfig(
    name='my-vm-1'
)

vm_config_2 = VMConfig(
    name='my-vm-2',
    num_cpus=2,
    memory=4096,
    disks={
        'root': 30,
        'data': 40
    },
    networks={
        'vm-lan-1': VMNetworkConfig(
            interface='ens192',
            ip_address='10.102.11.111/24'
        )
    },
    userdata_file='./userdata.yaml',
)

vsphere_config = VsphereConfig()

stack = VMwareStack(app, "stack-1", vsphere_config)
stack.create_vm(vm_config_1)
stack.create_vm(vm_config_2)


app.synth()
