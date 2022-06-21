from datetime import datetime

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
        if 'visited_today' not in request.COOKIES:
            # TODO: we need to track referers => request.META.get('HTTP_REFERER')
            self.store_ip_data(request)
            response = self.set_cookie(response, 'visited_today', True)
        return response

