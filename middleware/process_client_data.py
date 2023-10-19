from secrets import token_hex

from apps.geotracking.utils import Utils


class TrackVisitorMiddleware(Utils):
    """
    Set 'device_id' cookie for new visitors.

    On subsequent visits, the cookie is processed and a visitor is either registered or its record is updated.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if 'device_id' not in request.COOKIES:
            response = self.set_cookie(response, key='device_id', value=token_hex(16), expire_in=157680000)  # 5 years
        else:
            self.process_visitor(request)
        return response
