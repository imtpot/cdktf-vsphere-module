# cdktf-vsphere-module

A reusable Python module for provisioning VMs in VMware's vSphere platform using the Cloud Development Kit for Terraform (CDKtf).

## Features

- Simplified vSphere provisioning using Python.
- Abstraction over Terraform resources for easy usage.
- Create virtual machines based on specified configurations.
- Integration with CDKtf for deploying infrastructure-as-code.

## Prerequisites

- CDK for Terraform installed. [Installation Guide](https://learn.hashicorp.com/tutorials/terraform/cdktf-install)
- Terraform CLI installed.
- Necessary environment variables set (`VSPHERE_USER`, `VSPHERE_PASSWORD`, `VSPHERE_SERVER`).
- A vSphere environment with required resources (datastores, networks, templates, etc.).

## Usage with CDKtf

1. Initialize a new CDKtf project (if you haven't already):

```bash
cdktf init --providers vsphere --template python --local
```

2. Install the module using pipenv:
```bash
pipenv install -e "git+https://github.com/agmtr/cdktf-vsphere-module.git@main#egg=cdktf_vsphere_module" 
```

3. Import and use the vsphere_module in your main CDKtf application:
```python
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
```

3. Deploy the infrastructure:
```bash
cdktf deploy
```

This will start the process of provisioning the specified VM in your vSphere environment using Terraform.

## Contribution

Contributions, issues, and feature requests are welcome!

## License

MIT

## Acknowledgements

Thanks to the CDKTF and vSphere communities for providing the tools and resources to build this module.
