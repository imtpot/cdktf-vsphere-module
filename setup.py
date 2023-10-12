from setuptools import setup, find_packages

setup(
    name="cdktf_vsphere_module",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "cdktf",
        "cdktf-cdktf-provider-vsphere",
        "jinja2"
    ],
    include_package_data=True
)
