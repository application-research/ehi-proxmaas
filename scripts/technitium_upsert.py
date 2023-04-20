#!/usr/bin/env python3
import argparse
import json
import requests
import base64
from urllib.parse import urljoin

# Creates the DNS record in Technitium for just 1 domain

# Set up the argument parser
parser = argparse.ArgumentParser(description="Create DNS records for machines in Technitium DNS")
parser.add_argument('--dns_fqdn', type=str, required=True, help='The FQDN of the domain record being applied.')
parser.add_argument('--dns_record_type', type=str, required=True, help='The domain record type. Either A, AAAA or CNAME.')
parser.add_argument("--dns_record_value", required=True, help="Either an IP address or another hostname if using CNAME's")
parser.add_argument('--technitium_url', type=str, required=True, help='URL of Technitium DNS API')
parser.add_argument('--technitium_api_key', type=str, required=True, help='Technitium DNS API key')

# Parse the command-line arguments
args = parser.parse_args()

# Assign more readable variables
dns_fqdn = args.dns_fqdn
dns_subdomain = args.dns_fqdn.split('.')[0]
dns_base_domain = '.'.join(args.dns_fqdn.split('.')[1:])
dns_record_type = args.dns_record_type
dns_record_value = args.dns_record_value
technitium_url = args.technitium_url
technitium_api_key = args.technitium_api_key

# DEBUG
#print("dns_fqdn: " + str(dns_fqdn) + "\n\ndns_subdomain: " + str(dns_subdomain) + "\n\ndns_base_domain: " + str(dns_base_domain) + "\n\ndns_record_type: " + str(dns_record_type) + "\n\ndns_record_value: " + str(dns_record_value) + "\n\ntechnitium_url: " + str(technitium_url) + "\n\ntechnitium_api_key: " + str(technitium_api_key))

# Get existing DNS records
api_url = urljoin(technitium_url, "/api/zones/records/get")
query_params = {
    "token": technitium_api_key,
    "domain": dns_base_domain,
    "zone": dns_base_domain,
    "listZone": "true"
}
response = requests.get(api_url, params=query_params)
existing_records = response.json()

# DEBUG
#print("response.json(): " + str(response.json()))

# Get the list of existing records
existing_records_list = existing_records['response']['records']

# Check if the name exists in the existing_records_list
record_exists = any(record["name"] == dns_fqdn for record in existing_records_list)

if record_exists:
    print(f"{dns_fqdn} exists in the existing records. Moving on...")

elif ( not record_exists ) and ( dns_record_type == "CNAME" ):
    print(f"{dns_fqdn} does not exist in the existing records. Adding it now...")
    # Send a POST request to the Technitium API to add/update the record
    api_url = urljoin(technitium_url, "/api/zones/records/add")
    query_params = {
        "token": technitium_api_key,
        "domain": dns_fqdn,
        "zone": dns_base_domain,
        "type": dns_record_type,          
        "ttl": "3600",
        "cname": dns_record_value,
        "overwrite": "true"
    }
    response = requests.post(api_url, params=query_params)

    if response.status_code == 200:
        print(f"DNS record for {full_domain_name} created successfully.")
    else:
        print(f"Failed to create DNS record for {full_domain_name}. Response: {response.text}")

elif ( not record_exists ) and ( ( dns_record_type == "A" ) or ( dns_record_type == "AAAA" ) ):
    print(f"{dns_fqdn} does not exist in the existing records. Adding it now...")
    # Send a POST request to the Technitium API to add/update the record
    api_url = urljoin(technitium_url, "/api/zones/records/add")
    query_params = {
        "token": technitium_api_key,
        "domain": dns_fqdn,
        "zone": dns_base_domain,
        "type": dns_record_type,          
        "ttl": "3600",
        "ipAddress": dns_record_value,
        "overwrite": "true"
    }
    response = requests.post(api_url, params=query_params)

    if response.status_code == 200:
        print(f"DNS record for {dns_fqdn} created successfully.")
    else:
        print(f"Failed to create DNS record for {dns_fqdn}. Response: {response.text}")
