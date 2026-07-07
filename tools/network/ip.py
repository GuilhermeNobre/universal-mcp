import ipaddress


def validate_ip(value: str) -> str:
    """Validate an IPv4 or IPv6 address and describe it.

    Args:
        value: The IP address string to validate.
    """
    try:
        address = ipaddress.ip_address(value.strip())
    except ValueError:
        return f"'{value}' is not a valid IP address."

    traits = []
    if address.is_loopback:
        traits.append("loopback")
    if address.is_private:
        traits.append("private")
    if address.is_global:
        traits.append("global")
    if address.is_multicast:
        traits.append("multicast")
    if address.is_link_local:
        traits.append("link-local")
    if address.is_reserved:
        traits.append("reserved")

    return (
        f"'{address}' is a valid IPv{address.version} address.\n"
        f"Traits: {', '.join(traits) if traits else 'none'}"
    )


def cidr_info(cidr: str) -> str:
    """Describe a CIDR network: netmask, address range, and host count.

    Args:
        cidr: Network in CIDR notation, like 192.168.1.0/24 or 2001:db8::/32.
    """
    try:
        network = ipaddress.ip_network(cidr.strip(), strict=False)
    except ValueError:
        return f"'{cidr}' is not a valid CIDR network."

    lines = [
        f"Network: {network.network_address}/{network.prefixlen}",
        f"Netmask: {network.netmask}",
        f"Total addresses: {network.num_addresses}",
    ]

    if network.version == 4:
        lines.append(f"Broadcast: {network.broadcast_address}")
        if network.num_addresses > 2:
            usable = network.num_addresses - 2
            first_host = network.network_address + 1
            last_host = network.broadcast_address - 1
            lines.append(f"Usable hosts: {usable} ({first_host} - {last_host})")
        else:
            lines.append(f"Usable hosts: {network.num_addresses}")
    else:
        lines.append(f"Range: {network[0]} - {network[-1]}")

    return "\n".join(lines)


def ip_in_cidr(ip: str, cidr: str) -> str:
    """Check whether an IP address belongs to a CIDR network.

    Args:
        ip: The IP address to check.
        cidr: Network in CIDR notation, like 10.0.0.0/8.
    """
    try:
        address = ipaddress.ip_address(ip.strip())
    except ValueError:
        return f"'{ip}' is not a valid IP address."

    try:
        network = ipaddress.ip_network(cidr.strip(), strict=False)
    except ValueError:
        return f"'{cidr}' is not a valid CIDR network."

    if address.version != network.version:
        return f"'{ip}' is IPv{address.version} but '{cidr}' is IPv{network.version}."

    if address in network:
        return f"'{ip}' is inside '{cidr}'."
    return f"'{ip}' is NOT inside '{cidr}'."


TOOLS = [
    validate_ip,
    cidr_info,
    ip_in_cidr,
]
