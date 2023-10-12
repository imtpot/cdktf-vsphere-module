# helpers.py

import os
import re
from base64 import b64encode
from jinja2 import Environment, PackageLoader
from typing import Dict
from ..models.dataclasses import VMConfig


class ConfigService:
    SSH_KEY_PATTERN = r"^(ssh-rsa|ssh-dss|ssh-ed25519|ecdsa-sha2-nistp256) [A-Za-z0-9+/]+[=]{0,3}( .+)?$"

    @staticmethod
    def is_valid_ssh_key(ssh_key: str) -> bool:
        """Check if provided SSH key is valid."""
        return bool(re.match(ConfigService.SSH_KEY_PATTERN, ssh_key))

    @staticmethod
    def read_file_content(file_path: str) -> str:
        """Read and return content of the specified file."""
        try:
            with open(file_path, 'r') as file:
                return file.read().strip()
        except IOError as e:
            raise IOError(f"Error reading file: {file_path}. {str(e)}")

    @staticmethod
    def get_ssh_key_content(ssh_key_path: str) -> str:
        """Retrieve content of SSH key."""
        file_path = os.path.expanduser(ssh_key_path)
        if os.path.isfile(file_path):
            ssh_key_content = ConfigService.read_file_content(file_path)
            if not ConfigService.is_valid_ssh_key(ssh_key_content):
                raise ValueError(f"Invalid SSH key format in {file_path}")
            return ssh_key_content
        if ConfigService.is_valid_ssh_key(ssh_key_path):
            return ssh_key_path
        raise ValueError("Invalid SSH key format provided directly")

    @staticmethod
    def get_userdata_content(userdata_file: str) -> str:
        """Retrieve content of userdata file."""
        userdata_path = os.path.expanduser(userdata_file)
        if not os.path.isfile(userdata_path):
            raise FileNotFoundError(f"Userdata file {userdata_file} not found!")
        return ConfigService.read_file_content(userdata_path)

    @staticmethod
    def render_metadata_template(name: str, ssh_key: str, networks: dict) -> str:
        """Render metadata using provided template."""
        env = Environment(loader=PackageLoader("cdktf_vsphere_module", 'templates'), trim_blocks=True,
                          lstrip_blocks=True)
        template = env.get_template('metadata.yaml.j2')
        return template.render(name=name, ssh_key=ssh_key, networks=networks)

    @staticmethod
    def encode_content(content: str) -> str:
        """Encode content to base64."""
        return b64encode(content.encode()).decode()

    @staticmethod
    def generate_extra_config(vm_config: VMConfig) -> Dict[str, str]:
        """Generate additional configuration for VM."""
        ssh_key_content = ConfigService.get_ssh_key_content(vm_config.ssh_key)
        metadata_content = ConfigService.render_metadata_template(vm_config.name, ssh_key_content, vm_config.networks)
        encoded_metadata_content = ConfigService.encode_content(metadata_content)

        encoded_userdata_content = ""
        if vm_config.userdata_file:
            userdata_content = ConfigService.get_userdata_content(vm_config.userdata_file)
            encoded_userdata_content = ConfigService.encode_content(userdata_content)

        return {
            "guestinfo.metadata": encoded_metadata_content,
            "guestinfo.metadata.encoding": "base64",
            "guestinfo.userdata": encoded_userdata_content,
            "guestinfo.userdata.encoding": "base64"
        }
