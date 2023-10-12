# constants.py

from os import getenv


class VsphereConstants:
    """Constants for the vSphere provider."""
    USER = getenv("VSPHERE_USER")
    PASSWORD = getenv("VSPHERE_PASSWORD")
    SERVER = getenv("VSPHERE_SERVER")


class VMDefaults:
    """Default values for VM configuration."""
    DATACENTER = "Datacenter"
    CLUSTER = "dell-cluster-1"
    DATASTORE = "nfs_default_1"
    TEMPLATE = "rocky-9.2"
    SSH_KEY = "~/.ssh/id_ed25519.pub"
    FIRMWARE = "efi"

    CPUS = 1
    MEMORY = 512

    DISKS = {"root": 20}
    NETWORKS = {
        "vm-lan-1": {
            "interface": "ens192",
            "address": "dhcp"
        }
    }
