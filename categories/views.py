from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
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
            new_category = serializer.save()
            return Response(CategorySerializer(new_category).data)
        else:
            return Response(serializer.errors)


@api_view(["GET", "PUT"])
def category(request, id):
    try:
        category = Category.objects.get(pk=id)
    except Category.DoesNotExist:
        raise NotFound
    if request.method == "GET":
        data = CategorySerializer(category).data
        return Response(data)
    elif request.method == "PUT":
        data = CategorySerializer(
            category,
            data=request.data,
            partial=True,
        )
        if data.is_valid():
            updated_category = data.save()
            return Response(CategorySerializer(updated_category).data)
        else:
            return Response(data.errors)
