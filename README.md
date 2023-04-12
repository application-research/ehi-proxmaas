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

## Future features
### Additional ranges
We have left open the possibility of defining multiple ranges of IP addresses. A future version of the playbook will allow you to deploy machine groups across multiple IP ranges.

For example, instead of

```
list_of_ips:
  - start: 10.24.10.101
    end: 10.24.10.103
```

You might instead define

```
list_of_ips:
  - start: 10.24.10.101
    end: 10.24.10.103
  - start: 10.24.100.101
    end: 10.24.100.103
```

Actual implementation of these additional loops is not complete. PRs welcome.

### Automatically triggering playbooks upon a change
We will (eventually) implement a feature which chainloads playbooks specific to each inventory upon machines being created for that inventory folder.

This will allow you to define and deploy your whole infrastructure continuously.