#!/usr/bin/env python3

import sys
import json

# Load the JSON input
vm_data_json = sys.argv[1]
vm_data = json.loads(vm_data_json)

# Create a dictionary mapping VMIDs to MAC addresses
vmid_to_mac = {}
for vm in vm_data:
    vmid = vm['vmid']
    mac = vm['mac']['net0']
    vmid_to_mac[vmid] = mac

# Print the dictionary
print(vmid_to_mac)

# Write the dictionary to debug.log
with open('debug.log', 'w') as f:
    f.write(str(vmid_to_mac))
    f.close()