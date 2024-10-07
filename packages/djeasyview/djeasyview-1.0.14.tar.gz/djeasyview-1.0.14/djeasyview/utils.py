import io

from django.core.paginator import Paginator
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer

from rest_framework.response import Response
from rest_framework.serializers import Serializer
from django.db.models import QuerySet
from .response import SuccessResponse


def paginator(serializer, per_page):
    return Paginator(message_parser(serializer), per_page=per_page)


# ordered dict to json converter
def message_parser(data):
    result_data = JSONRenderer().render(data)
    init_streams = io.BytesIO(result_data)
    return JSONParser().parse(init_streams)


def paginated_views(
    page_size: str, page_number: str, serializer: Serializer, queryset: QuerySet
) -> Response:
    if page_number and page_size:
        paginator_record = paginator(serializer, page_size)
        paginated_data = paginator_record.page(page_number).object_list
        return SuccessResponse(
            {
                "total_count": queryset.count(),
                "queryset_count": len(paginated_data),
                "data": paginated_data,
            }
        )
