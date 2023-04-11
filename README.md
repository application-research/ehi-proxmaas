# Cloudy Dreams for EHI
This is an experimental repo intended to enable the spawning of arbitrary machines in EHI using Proxmox and MAAS.

## Prerequisites
* A working EHI environment including Proxmox and MAAS
* Credentials for the Proxmox and MAAS APIs
* A "client" machine with the following Python3 modules installed
    * `proxmoxer`
    * `requests`

## Getting started
1. Clone this repo
2. Copy vars/secrets.yml.dist to vars/secrets.yml
3. Edit vars/secrets.yml to include your Proxmox and MAAS credentials
4. Run `ansible-playbook spawn.yml`