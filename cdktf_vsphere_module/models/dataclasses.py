# dataclasses.py

from dataclasses import dataclass, field
from typing import List, Dict, Optional
from ..config.constants import VsphereConstants, VMDefaults


@dataclass
class VsphereConfig:
    """Dataclass for vSphere configurations."""
    user: str = VsphereConstants.USER
    password: str = VsphereConstants.PASSWORD
    vsphere_server: str = VsphereConstants.SERVER
    allow_unverified_ssl: bool = True


@dataclass
class VMNetworkConfig:
    """Dataclass for VM network configurations."""
    interface: str
    ip_address: Optional[str] = None
    gateway: Optional[str] = None
    dns: Optional[List[str]] = None


@dataclass
class VMConfig:
    """Dataclass for VM configurations."""
    name: str
    num_cpus: Optional[int] = VMDefaults.CPUS
    memory: Optional[int] = VMDefaults.MEMORY
    disks: Optional[Dict[str, int]] = field(default_factory=VMDefaults.DISKS.copy)
    networks: Dict[str, VMNetworkConfig] = field(default_factory=VMDefaults.NETWORKS.copy)
    template: str = VMDefaults.TEMPLATE
    ssh_key: str = VMDefaults.SSH_KEY
    firmware: str = VMDefaults.FIRMWARE
    userdata_file: Optional[str] = None
    datacenter: str = VMDefaults.DATACENTER
    cluster: str = VMDefaults.CLUSTER
    datastore: str = VMDefaults.DATASTORE
