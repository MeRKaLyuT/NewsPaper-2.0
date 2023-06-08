import sys
import pytz
from django.utils import timezone


class SimpleMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        print(sys.platform)
        # код, выполняемый до формирования ответа (или другого middleware)

        response = self.get_response(request)

        # код, выполняемый после формирования запроса (или нижнего слоя)

        return response


class TimezoneMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        tzname = request.session.get('django_timezone')

        if tzname:
            timezone.activate(pytz.timezone(tzname))
        else:
            timezone.deactivate()
        return self.get_response(request)
