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

## Notes for later
scp wings@prod-tls-gen:/home/wings/.lego/certificates/_.estuary.tech.issuer.crt .
wings@chase:~/projects/wildcard-tls-playbook$ scp _.estuary.tech.issuer.crt wings@prod-ebi-maas01:/home/wings/
root@prod-ebi-maas01:/var/snap/maas/common/keys# cp ~wings/_.estuary.tech.issuer.crt cacert.pem
root@prod-ebi-maas01:/var/snap/maas/common/keys# maas config-tls enable --cacert cacert.pem /var/snap/maas/common/keys/maas.key /var/snap/maas/common/keys/maas.crt --port 443^C
