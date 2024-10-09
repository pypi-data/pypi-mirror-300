from lat_lon_parser import parse


def build_tenant_name(client_id, name):
    if client_id and name:
        return f"{client_id} - {name}"[0:100].strip()
    elif client_id:
        return f"{client_id}"
    else:
        return f"{name}"[0:100].strip()


def sanitize_lat_lon(lat_or_lon: str) -> float:
    """
    Gets latitude or longitude string and returns float with 6 decimal places
    This format is required in Netbox
    """
    if not lat_or_lon:
        return None

    try:
        result = parse(lat_or_lon)
    except ValueError:
        return None

    if result:
        return round(result, 6)
    else:
        return None
