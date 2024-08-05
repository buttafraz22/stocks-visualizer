from rest_framework.pagination import PageNumberPagination

class SymbolAPIPagination(PageNumberPagination):
    page_size = 10
    max_page_size = 20

    def get_page_size(self, request):
        page_size = request.query_params.get('page_size')
        if not page_size:
            return self.page_size

        if not page_size.isdigit():
            return self.page_size
        
        return int(page_size)
    
    def get_page_number(self, request, paginator):
        page_number = request.query_params.get('page', 1)
        if page_number in self.last_page_strings:
            page_number = paginator.num_pages
        return page_number