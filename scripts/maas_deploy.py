#!/usr/bin/env python3
import argparse
import json
from maas.client import connect
from maas.client.enum import LinkMode
import configparser
from os.path import expanduser

# Set up the argument parser
parser = argparse.ArgumentParser(description="Set Proxmox token ID and secret for a machine in MAAS")
parser.add_argument('--vm_details', type=str, required=True, help='VM details from Ansible')

# Parse the command-line arguments
args = parser.parse_args()

# Set up the config parser
config = configparser.ConfigParser()
config.read(expanduser("~/.proxmox-maas.cfg"))

# Connect to MAAS
client = connect("https://maas.estuary.tech/MAAS", apikey=config["maas_api"]["api_key"])

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
    # If we've defined IP addresses, force a static assignment
    if "ipv4" in vm:
        # Read the list of subnets
        subnets = client.subnets.list()
        subnet = None
        for s in subnets:
            if s.cidr == "10.24.0.0/16":
                subnet = s
                break
        # Set interface to be the machine interface
        # TODO(bug): Make this work with more than one interface defined, add flexibility etc
        for interface in machine.interfaces:
            # Update the IP address
            interface.links.create(ip_address=vm["ipv4"], mode=LinkMode.STATIC, subnet=subnet, default_gateway=True, force=True)
    # Check the power on the machine to update its BMC status
    machine.query_power_state()
    # Deploy the machine
    machine.deploy()
