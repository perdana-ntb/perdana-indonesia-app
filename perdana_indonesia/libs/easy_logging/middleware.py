import json
from json.decoder import JSONDecodeError
from typing import Dict, List, Tuple

from django.conf import settings
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.utils.deprecation import MiddlewareMixin
from ipware import get_client_ip

from easy_logging.models import EasyLogging


class EasyLoggingMiddleware(MiddlewareMixin):

    def __init__(self, get_response) -> None:
        super().__init__(get_response=get_response)
        if not settings.EASY_LOGGING_ENDPOINT_CATCH_ALL and \
                not settings.EASY_LOGGING_USE_METHOD_INSTEAD:
            if not isinstance(settings.EASY_LOGGING_ENDPOINT_CONTAINS, (Tuple, List)):
                raise Exception('EASY_LOGGING_ENDPOINT_CONTAINS should be List or Tuple')

            if len(settings.EASY_LOGGING_ENDPOINT_CONTAINS) < 1:
                raise Exception('EASY_LOGGING_ENDPOINT_CONTAINS should contains 1 or more endpoint')

        if not settings.EASY_LOGGING_METHOD_CATCH_ALL and settings.EASY_LOGGING_USE_METHOD_INSTEAD:
            if not isinstance(settings.EASY_LOGGING_CATCH_METHODS, (Tuple, List)):
                raise Exception('EASY_LOGGING_CATCH_METHODS should be List or Tuple')

            if len(settings.EASY_LOGGING_CATCH_METHODS) < 1:
                raise Exception('EASY_LOGGING_CATCH_METHODS should contains 1 or more method')

    def _getUsername(self, request: HttpRequest) -> str:
        if request.user.is_authenticated:
            return request.user.username
        return 'Anonymous'

    def _checkLoggingAllowance(self, request: HttpRequest) -> bool:
        if settings.EASY_LOGGING_ALLOW_ANONYMOUS:
            return True
        return request.user.is_authenticated

    def _getIpAddress(self, request: HttpRequest) -> str:
        clientIp, _ = get_client_ip(request)
        return clientIp

    def _checkLoggingScope(self, request: HttpRequest) -> EasyLogging:
        if self._checkLoggingAllowance(request):
            username = self._getUsername(request)
            ipAddress = self._getIpAddress(request)
            instance = EasyLogging(
                username=username,
                endpoint=request.path,
                method=request.method,
                ip_address=ipAddress,
                request_json=request.POST.dict(),
                kwargs=request.headers.__dict__
            )

            if settings.EASY_LOGGING_ENDPOINT_CATCH_ALL:
                instance.save()
            elif request.path in settings.EASY_LOGGING_ENDPOINT_CONTAINS:
                instance.save()
            elif settings.EASY_LOGGING_METHOD_CATCH_ALL:
                instance.save()
            elif request.method in settings.EASY_LOGGING_CATCH_METHODS:
                instance.save()

            return instance

    def _collectResponse(self, response: HttpResponse) -> Dict:
        if hasattr(response, 'json') and response.json():
            return response.json()

        try:
            return json.loads(response.content)
        except JSONDecodeError:
            return {}

    def __call__(self, request: HttpRequest) -> HttpResponse:
        response = super().__call__(request)
        instance: EasyLogging = self._checkLoggingScope(request)
        if instance and instance.pk:
            instance.response_json = self._collectResponse(response)
            instance.save()

        return response
