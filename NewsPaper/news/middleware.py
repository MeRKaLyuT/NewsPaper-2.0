import sys


class SimpleMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        print(sys.platform)
        # код, выполняемый до формирования ответа (или другого middleware)

        response = self.get_response(request)

        # код, выполняемый после формирования запроса (или нижнего слоя)

        return response