
# ProxMAAS Quick Start Guide

ProxMAAS allows for you to define virtual hosts in variable files and then create them automatically. New hosts will be created on Proxmox and managed by MAAS.


## Creating VMs

1) In the ehi-proxmaas playbook, create a new variable file that defines the new host you want to make:
```
pcadmin@workstation:~/projects/estuary-hosted-infrastructure$ cat ./playbooks/ehi-proxmaas/vars/production-ehi/prod-garage.yml 
---
# Machine specs
scsi_disk_layout:
  scsi0: "vm-storage:300,format=raw,discard=on,ssd=1"
amount_of_memory: 8192
number_of_vcpus: 8
ip_range:
  - start: 10.24.3.235
    end: 10.24.3.235
starting_number: 1
vm_name: prod-garage
vm_description: "Production GarageHQ S3"
dns_record_type: "A"		# Variables for Technitium DNS, no record will be created if 'dns_record_type' is not defined
```

2) Run the spawn.yml playbook in ProxMAAS and define a {{ machine_details }} variable like so:
```
pcadmin@workstation:~/projects/estuary-hosted-infrastructure$ ansible-playbook-ehi playbooks/ehi-proxmaas/spawn.yml --vault-id proxmaas@~/.ehi-vault/proxmaas --extra-vars "machine_details=prod-garage"
```


## Destroying VMs

The process for destroying VMs is quite similar, you just need to ensure the VMs in questions are shut off and prepare to answer the following interactive questions:

```
pcadmin@workstation:~/projects/estuary-hosted-infrastructure$ ansible-playbook-ehi playbooks/ehi-proxmaas/destroy.yml --vault-id proxmaas@~/.ehi-vault/proxmaas  --extra-vars "machine_details=prod-garage"
...

TASK [Set the VM name for the VMs] **************************************************************************************************************************************
[Set the VM name for the VMs]
Enter the VM name for the VMs you want to destroy. PERMANENTLY!:
prod-garage
...
TASK [Set the starting number for the VMs] ******************************************************************************************************************************
[Set the starting number for the VMs]
Enter the starting number for the VMs (e.g. 01 if it's a new deployment, 04 if there are already 3 machines, etc.):
01
...
TASK [Set the starting number for the VMs] ******************************************************************************************************************************
[Set the starting number for the VMs]
Enter the number of VMs you want to DESTROY:
1
...
TASK [Ask the user if they wish to continue] ****************************************************************************************************************************
[Ask the user if they wish to continue]
Are you completely sure you wish to continue? (yesiamsure/n):
yesiamsure
```