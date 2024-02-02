from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Category
from .serializers import CategorySerializer

# Create your views here.


@api_view()
def categories(request):
    data = CategorySerializer(
        Category.objects.all(),
        many=True,
    ).data
    return Response(
        {
            "ok": True,
            "categories": data,
        }
    )
