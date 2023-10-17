from datetime import datetime

from secrets import token_hex

from apps.geotracking.utils import Utils


class ProcessClientDataMiddleware(Utils):

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        """
        All processing is based on 'visited_today' cookie, which expires at midnight.
        If this cookie doesn't exist (expired), then a new one is set,
        after the execution of the following processes:
         - IP info is obtained (if routable) and stored in the database
        """
        response = self.get_response(request)
        if 'device_id' not in request.COOKIES:
            # TODO: we need to track referers => request.META.get('HTTP_REFERER')
            response = self.set_cookie(response, key='device_id', value=token_hex(16))
        else:
            # IP address is stored upon a new visit (legitimate user?)
            self.register_visitor(request)
        return response

