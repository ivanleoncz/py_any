from datetime import datetime

from apps.geotracking.utils import Utils


class TrackVisitIpMiddleware(Utils):

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # before view call...
        if 'visited_today' not in request.COOKIES:
            self.store_ip_data(request)
        response = self.get_response(request)
        # after view call...
        if 'visited_today' not in request.COOKIES:
            # Cookie should expire at 00:00:00 (seconds precision is not guaranteed)
            dt_diff = f"{23 - datetime.utcnow().hour}:{60 - datetime.utcnow().minute}:{60 - datetime.utcnow().second}"
            dt = datetime.strptime(dt_diff, '%H:%M:%S')
            response = self.set_cookie(response, 'visited_today', True, expire=(dt.hour * 60 + dt.minute) * 60)

        return response

