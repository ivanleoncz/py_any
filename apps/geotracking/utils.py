import json
import requests

ip_database_provider = "http://ipinfo.io/"


def get_ip_data(ip_address: str) -> dict:
    """
    Searches and obtains IP metadata.

    parameters
    ---------
    ip_address : str

    returns
    -------
    IP address metadata, filtered via list comprehension over JSON response as dictionary.
    """
    r = requests.get("".join(ip_database_provider, ip_address))
    # For returning more information on data dict, just add IPINFO fields on list comprehension's tuple...
    data = {k: v for k, v in json.loads(r.content.decode()).items() if k in ('country', 'city', )}
    return data
