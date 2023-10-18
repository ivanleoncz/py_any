from datetime import datetime
from ipaddress import ip_network
import json
import random

from django.conf import settings
from ipware import get_client_ip
import requests

from .models import Visitor


class Utils:

    @staticmethod
    def get_random_public_ip() -> str:
        """
        Returns a random public/global IPv4 address from a short list of IPs. Used for testing purposes.
        """
        random.seed(random.randint(0, 1000))
        random_ips = list(ip_network('123.25.44.0/28').hosts())
        random_ips += list(ip_network('25.1.4.128/28').hosts())
        random_ips += list(ip_network('13.250.24.0/28').hosts())
        random_ips += list(ip_network('78.21.94.128/28').hosts())
        return random.choice(random_ips).__str__()

    @staticmethod
    def get_ip_data(ip_address: str) -> dict:
        """
        Searches and obtains IP metadata.

        In order to obtain other response data for an IP address, referrer to this document and adjust 'fields' tuple:
        - https://ipinfo.io/developers/responses#full-response

        returns
        -------
        IP address metadata
        """
        fields = ('country', 'city', )
        response = requests.get("".join((settings.IP_DATA_PROVIDER, ip_address)))
        return {k: v for k, v in json.loads(response.content.decode()).items() if k in fields}

    def register_visitor(self, request: dict) -> None:
        """
        Stores visitor and its metadata ('device_id' cookie, ip, referrer, etc.).

        Parameters
        ----------
        request
            Django request object.
        """
        client_ip, is_routable = get_client_ip(request)
        if is_routable:
            visitor, created = Visitor.objects.get_or_create(device_id=request.COOKIES["device_id"],
                                                             defaults={"ip_address": client_ip,
                                                                       "referrer": request.META.get('HTTP_REFERER')})
            if created:
                data = self.get_ip_data(client_ip)
                if data:
                    visitor.country = data.get("country", "???")
                    visitor.city = data.get("city", "???")
                    visitor.days_visited = 1
                    visitor.save()
            else:
                if visitor.updated.date() != datetime.now().date():
                    # Once visitor.updated is equal today, then no more increment is performed.
                    visitor.days_visited += 1
                    visitor.save()

    @staticmethod
    def set_cookie(response, key: str, value, expire_in: int = None) -> str:
        """
        Sets a cookie on Django's response object and its expiry time.

        If expire_in is not provided, cookie max age lasts until midnight (00:00:00) UTC, through the following formula:
            (Remaining Hours -> Minutes + Remaining Minutes) as Seconds - Remaining Seconds

        Parameters
        ----------
        response: response object from Django
        key: cookie name
        value: cookie value
        expire_in: cookie max age in secs

        Returns
        -------
        response object with the defined cookie and its expiration
        """
        if expire_in:
            max_age = expire_in
        else:
            ts = datetime.utcnow()
            max_age = (((23 - ts.hour) * 60) + (60 - ts.minute)) * 60 - ts.second
        response.set_cookie(key, value, max_age=max_age, domain=settings.SESSION_COOKIE_DOMAIN,
                            secure=settings.SESSION_COOKIE_SECURE or None)
        return response
