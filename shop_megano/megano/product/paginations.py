from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination


class SetSalesPagePagination(PageNumberPagination):
    """
    Класс пагинация страниц сайта у распродажи.
    """

    page_size = 3
    page_query_param = "currentPage"
    max_page_size = 3

    def get_paginated_response(self, data):
        # print(self.page.__dict__)
        return Response(
            {
                "items": data,
                "currentPage": self.page.number,
                "lastPage": self.page.paginator.num_pages,
            }
        )


class SetPagePagination(PageNumberPagination):
    """
    Класс пагинация страниц сайта у каталога.
    """

    page_size = 8
    page_query_param = "currentPage"
    max_page_size = 8

    def get_paginated_response(self, data):
        # print(self.page.__dict__)
        return Response(
            {
                "items": data,
                "currentPage": self.page.number,
                "lastPage": self.page.paginator.num_pages,
            }
        )
