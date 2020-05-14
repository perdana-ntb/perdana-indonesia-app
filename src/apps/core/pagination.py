from rest_framework import pagination
from rest_framework.response import Response


class CustomPageNumberPagination(pagination.PageNumberPagination):
    page_size = 20

    def get_paginated_response(self, data):
        return Response({
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'page': self.page.number,
            'total_pages': self.page.paginator.num_pages,
            'total_results': self.page.paginator.count,
            'results': data
        })
