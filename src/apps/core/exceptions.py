from rest_framework.exceptions import APIException


class PerdanaError(APIException):
    status_code = 400
    detail = 'Bad Request'

    def __init__(self, *args, **kwargs):
        if kwargs.get('status_code'):
            self.status_code = kwargs.get('status_code')
        if kwargs.get('message'):
            self.detail = kwargs.get('message')
