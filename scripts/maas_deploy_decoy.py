#!/usr/bin/env python3
import argparse
import json
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

# Load the VM details from the JSON object we were passed
vm_details = json.loads(args.vm_details)

# Write the vm_details we were given to $HOME/vm_details.json
with open(expanduser("~/vm_details.json"), 'w') as vm_details_file:
    json.dump(vm_details, vm_details_file)
