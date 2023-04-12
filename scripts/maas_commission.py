#!/usr/bin/env python3
import argparse
import json
from maas.client import connect
import configparser
from os.path import expanduser

# Set up the argument parser
parser = argparse.ArgumentParser(description="Set Proxmox token ID and secret for a machine in MAAS")
parser.add_argument('--proxmox_token_id', type=str, required=True, help='Proxmox token ID/name')
parser.add_argument('--proxmox_token_secret', type=str, required=True, help='Proxmox token secret')
parser.add_argument('--proxmox_user', type=str, required=True, help='Proxmox user including realm (eg root@pam)')
parser.add_argument('--vm_details', type=str, required=True, help='VM details from Ansible')

# Parse the command-line arguments
args = parser.parse_args()

# DEBUG: Write a copy of the VM details to a file
with open("/root/vm_details.json", "w") as f:
    f.write(args.vm_details)
    f.close

# Set up the config parser
config = configparser.ConfigParser()
config.read(expanduser("~/.proxmox-maas.cfg"))

# Connect to MAAS
client = connect("https://maas.estuary.tech/MAAS", apikey=config["maas_api"]["api_key"])
tmpl = "{0.hostname} {1.name} {1.mac_address}"

# Get a list of all machines and their MAC addresses
machine_mac_addresses = {}
for machine in client.machines.list():
    for interface in machine.interfaces:
        machine_mac_addresses[interface.mac_address] = { "system_id": machine.system_id, "name": machine.hostname }

# Iterate through the data in vm_details
target_mac_address = None

# Load the VM details from the JSON object we were passed
vm_details = json.loads(args.vm_details)

# For machine with this MAC, set all the correct parameters
for vm_key in vm_details:
    vm = vm_details[vm_key]
    target_mac_address = vm["mac"]["net0"].lower()
    machine = client.machines.get(system_id=machine_mac_addresses[target_mac_address]["system_id"])
    machine.hostname = vm["name"]
    # machine.power_type="proxmox"
    machine.set_power(power_type="proxmox", power_parameters={
    "power_address": "https://proxmox.estuary.tech:8006",
    "power_user": args.proxmox_user,
    "power_token_name": args.proxmox_token_id,
    "power_token_secret": args.proxmox_token_secret,
    "power_vm_name": vm_key,
    "power_verify_ssl": "n"
    })
    machine.save()
    # Check the power on the machine to update its BMC status
    machine.query_power_state()
    # Commission the machine
    machine.commission(commissioning_scripts=[])
