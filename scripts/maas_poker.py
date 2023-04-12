#!/usr/bin/env python3
# pokes MAAS

# TASK [Display the vmid_to_mac dictionary] **********************************************************
# ok: [localhost] => {
#     "vmid_to_mac": {
#         "133": {
#             "net0": "A2:F2:24:9A:6C:0F"
#         },
#         "134": {
#             "net0": "7E:ED:FE:67:F2:75"
#         }
#     }
# }

import configparser
import os
from os.path import expanduser
from oauthlib.oauth1 import SIGNATURE_PLAINTEXT
from requests_oauthlib import OAuth1Session

MAAS_HOST = "https://maas.estuary.tech/MAAS"
config = configparser.ConfigParser()
config.read(expanduser("~/.proxmox-maas.cfg"))

CONSUMER_KEY, CONSUMER_TOKEN, SECRET = config["maas_api"]["api_key"].split(":")

maas = OAuth1Session(CONSUMER_KEY, resource_owner_key=CONSUMER_TOKEN, resource_owner_secret=SECRET, signature_method=SIGNATURE_PLAINTEXT)

mac_address = "A2:F2:24:9A:6C:0F"
response = maas.get(f"{MAAS_HOST}/api/2.0/devices/", params={"mac_address": mac_address})
response.raise_for_status()

print(response.json())

