import ipaddress
import socket
from typing import Any

import psutil


def get_ip(nic_name: str = 'WLAN') -> str:
    return get_address_info(nic_name).address


def get_netmask(nic_name: str = 'WLAN') -> str:
    return get_address_info(nic_name).netmask


def get_broadcast(nic_name: str = 'WLAN') -> str:
    ip = get_ip(nic_name)
    netmask = get_netmask(nic_name)
    network = ipaddress.ip_network(f'{ip}/{netmask}', strict=False)
    return network.broadcast_address.exploded


def get_address_info(nic_name) -> Any:
    for name, named_tuples in psutil.net_if_addrs().items():
        if name == nic_name:
            for named_tuple in named_tuples:
                if named_tuple.family == socket.AF_INET:
                    return named_tuple
