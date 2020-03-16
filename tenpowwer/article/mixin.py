from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class MeiduoPagination(PageNumberPagination):
    # 后端指定每页显示数量
    page_size = 5
    # 查询参数的key
    page_query_param = 'page'
    # 每页最大个数
    max_page_size = 10
    def get_paginated_response(self,data):
        return Response({
            'count': self.page.paginator.count,  # 总数量
            'results': data,  # 用户数据
            'next': self.get_next_link(),  # 当前页数
            'previous': self.get_previous_link(),  # 总页数
        })