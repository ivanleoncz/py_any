from datetime import datetime
from ipaddress import ip_network
import json
import random

from ipware import get_client_ip
import requests

from .models import Visitor

ip_database_provider = "http://ipinfo.io/"


class Utils:

    @staticmethod
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
        r = requests.get("".join((ip_database_provider, ip_address)))
        # For returning more information on data dict, just add IPINFO fields on list comprehension's tuple...
        data = {k: v for k, v in json.loads(r.content.decode()).items() if k in ('country', 'city', )}
        return data

    def store_ip_data(self, request: dict) -> None:
        """
        Stores the IP data at Visitors model, if any data is available via Utils.get_ip_data().

        Parameters
        ----------
        request
            Django default request object.
        """
        client_ip, is_routable = get_client_ip(request)
        if is_routable:
            visitor, created = Visitor.objects.get_or_create(ip=client_ip)
            if created:
                # When created, the visitor data gets updated with data available
                # via ipinfo request response data...
                data = self.get_ip_data(client_ip)  # Searching for IP data
                if data:
                    visitor.country = data.get("country", "???")
                    visitor.city = data.get("city", "???")
                    visitor.save()
            else:
                # Already registered visitor get amount_of_requests incremented (see models.py)
                # only if her/his visit wasn't today...
                if visitor.last_request.date() != datetime.now().date():
                    visitor.save()

    @staticmethod
    def get_random_public_ip() -> str:
        """
        Returns a random public/global IPv4 address from a short list of IPs.
        """
        random.seed(random.randint(0, 1000))
        random_ips = list(ip_network('123.25.44.0/28').hosts())
        random_ips += list(ip_network('25.1.4.128/28').hosts())
        random_ips += list(ip_network('13.250.24.0/28').hosts())
        random_ips += list(ip_network('78.21.94.128/28').hosts())
        return random.choice(random_ips).__str__()
