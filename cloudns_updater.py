# -*- coding: utf-8 -*-
""" ClouDNS Updater """

__version__ = "1.0.0"
__author__ = "Jonathan Gonzalez"
__email__ = "j@0x30.io"
__date__ = "2023-02-20"

# pylint: disable=W0703,C0301

# - Standard libraries
from typing import Any, Dict, List

# - Third-party libraries
import requests

# - ---------------------------------------------------------------------------
# - PLEASE, CONFIGURE THE FOLLOWING FOUR (4) VARIABLES WITH YOUR OWN DETAILS
# - ---------------------------------------------------------------------------

# - Variables
_CLOUDNS_AUTH_ID: str = "NNNN"
_CLOUDNS_AUTH_PASSWORD: str = "aaaabbbbccccddddeeeeffffgggghhhhiiiijjjjkkkkllll"
_CLOUDNS_DOMAIN_NAME: str = "domain.tld"
_CLOUDNS_HOSTNAME: str = "hostname"


# - ---------------------------------------------------------------------------
# - WARNING: DO NOT CHANGE ANYTHING BELOW THIS POINT
# - ---------------------------------------------------------------------------


def get_current_ip() -> str:
    """Obtain currently configured IP

    Returns:
        str: IP address currently configured in ClouDNS servers
    """
    response: str = ""
    payload: Dict[str, str] = {"auth-id": _CLOUDNS_AUTH_ID, "auth-password": _CLOUDNS_AUTH_PASSWORD}

    try:
        resp = requests.get("https://api.cloudns.net/ip/get-my-ip.json", params=payload, timeout=60)
        response = dict(resp.json())["ip"]
    except requests.ConnectionError as conn_err:
        print(f"Error: {conn_err}")
    except Exception as broad_err:
        print(f"Error: {broad_err}")

    return response


def get_dns_record() -> List[str]:
    """Obtain DNS record for the domain in use

    Returns:
        List[str]: Obtains the ClouDNS record for an specific domain/host
    """
    response: List[str] = []
    payload: Dict[str, str] = {
        "auth-id": _CLOUDNS_AUTH_ID,
        "auth-password": _CLOUDNS_AUTH_PASSWORD,
        "domain-name": _CLOUDNS_DOMAIN_NAME,
        "host": _CLOUDNS_HOSTNAME,
    }

    try:
        resp = requests.get("https://api.cloudns.net/dns/records.json", params=payload, timeout=60)
        zone_record_id: str = list(resp.json())[0]
        dns_data: Dict[Any, Any] = resp.json()
        record_data: Any = dns_data[zone_record_id]
        dns_ip: str = record_data.get("record")
        response = [zone_record_id, dns_ip]
    except requests.ConnectionError as conn_err:
        print(f"Error: {conn_err}")
    except Exception as broad_err:
        print(f"Error: {broad_err}")

    return response


def update_dns_record(*args) -> str:
    """Update the DNS record with the new IP detected

    Returns: a string indicating actions performed in ClouDNS records
    """
    response: str = ""
    payload: Dict[str, str] = {
        "auth-id": _CLOUDNS_AUTH_ID,
        "auth-password": _CLOUDNS_AUTH_PASSWORD,
        "domain-name": _CLOUDNS_DOMAIN_NAME,
        "host": _CLOUDNS_HOSTNAME,
        "record-id": args[0],  # this is the Record-ID
        "record": args[1],  # this is the IP Address
        "ttl": "60",
    }

    try:
        resp = requests.post("https://api.cloudns.net/dns/mod-record.json", params=payload, timeout=60)
        response = resp.text
    except requests.ConnectionError as conn_err:
        print(f"Error: {conn_err}")
    except Exception as broad_err:
        print(f"Error: {broad_err}")

    return response


def main() -> None:
    """Main loop

    Returns: None
    """
    _current_ip: str = get_current_ip()
    _dns_record: List[str] = get_dns_record()
    print(f"Current IP: {_current_ip}")
    print(f"IP found in DNS: {_dns_record[1]}")

    if _dns_record[1] != _current_ip:
        print("-> Updaing IP in DNS.")
        response: str = update_dns_record(_dns_record[0], _current_ip)
        print(f"-> ClouDNS response data: {response}")
    else:
        print("-> Same IP, nothing to change.")


if __name__ == "__main__":
    main()
