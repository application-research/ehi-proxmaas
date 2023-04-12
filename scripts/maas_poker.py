#!/usr/bin/env python3
# pokes MAAS

# ok: [localhost] => {
#     "vm_details": {
#         "133": {
#             "mac": {
#                 "net0": "F6:59:F9:7F:AF:48"
#             },
#             "name": "dev-test01"
#         },
#         "134": {
#             "mac": {
#                 "net0": "32:8C:68:96:BE:F2"
#             },
#             "name": "dev-test02"
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

mac_address = "f6:59:f9:7f:af:48"
response = maas.get(f"{MAAS_HOST}/api/2.0/devices/", params={"mac_address": mac_address})
response.raise_for_status()

print(response.json())

