from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Category
from .serializers import CategorySerializer

# Create your views here.


@api_view(["GET", "POST"])
def categories(request):
    if request.method == "GET":
        data = CategorySerializer(
            Category.objects.all(),
            many=True,
        ).data
        return Response(data)
    elif request.method == "POST":
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            return Response({"created": True})
        else:
            return Response(serializer.errors)


@api_view()
def category(request, id):
    category = Category.objects.get(pk=id)
    data = CategorySerializer(category).data
    return Response(data)
