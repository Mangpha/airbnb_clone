from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.views import APIView
from rest_framework.status import HTTP_204_NO_CONTENT
from .models import Category
from .serializers import CategorySerializer

# Create your views here.


class Categories(APIView):
    def get(self, request):
        data = CategorySerializer(
            Category.objects.all(),
            many=True,
        ).data
        return Response(data)

    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            new_category = serializer.save()
            return Response(CategorySerializer(new_category).data)
        else:
            return Response(serializer.errors)


class CategoryDetail(APIView):
    def get_object(self, id):
        try:
            category = Category.objects.get(pk=id)
        except Category.DoesNotExist:
            raise NotFound
        return category

    def get(self, request, id):
        return Response(CategorySerializer(self.get_object(id)).data)

    def put(self, request, id):
        data = CategorySerializer(
            self.get_object(id),
            data=request.data,
            partial=True,
        )
        if data.is_valid():
            updated_category = data.save()
            return Response(CategorySerializer(updated_category).data)
        else:
            return Response(data.errors)

    def delete(self, request, id):
        self.get_object(id).delete()
        return Response(status=HTTP_204_NO_CONTENT)
