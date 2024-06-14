from rest_framework import pagination


class LodgingPaginator(pagination.PageNumberPagination):
    page_size = 5

