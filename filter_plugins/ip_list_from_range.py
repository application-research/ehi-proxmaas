#!/usr/bin/env python3
from ansible.errors import AnsibleError
import ipaddress

def ip_list_from_range(start_ip, end_ip):
    try:
        start_ip_int = int(ipaddress.IPv4Address(start_ip))
        end_ip_int = int(ipaddress.IPv4Address(end_ip))
        return [str(ipaddress.IPv4Address(ip)) for ip in range(start_ip_int, end_ip_int + 1)]
    except Exception as e:
        raise AnsibleError(f"Error generating IP list: {e}")

class FilterModule(object):
    def filters(self):
        return {
            'ip_list_from_range': ip_list_from_range
        }