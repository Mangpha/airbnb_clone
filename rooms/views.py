# Django Import
from django.db import transaction
from django.conf import settings

# DRF Import
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import (
    NotFound,
    NotAuthenticated,
    ParseError,
    PermissionDenied,
)
from rest_framework.status import HTTP_204_NO_CONTENT

# Model Import
from .models import Amenity, Room
from reviews.models import Review
from categories.models import Category

# Serializers Import
from reviews.serializers import ReviewSerializer
from medias.serializers import PhotoSerializer
from .serializers import AmenitySerializer, RoomListSerializer, RoomDetailSerializer

# Create your views here.


class Rooms(APIView):

    def get(self, request):
        all_rooms = Room.objects.all()
        return Response(
            RoomListSerializer(
                all_rooms,
                many=True,
                context={"request": request},
            ).data
        )

    def post(self, request):
        if request.user.is_authenticated:
            serializer = RoomDetailSerializer(data=request.data)
            if serializer.is_valid():
                category_id = request.data.get("category")
                if not category_id:
                    raise ParseError("Category is required.")
                try:
                    category = Category.objects.get(pk=category_id)
                    if category.kind == Category.CategoryKindChoices.EXPERIENCES:
                        raise ParseError("The category kind should be 'rooms'.")
                except Category.DoesNotExist:
                    raise ParseError("Category not found.")
                try:
                    with transaction.atomic():
                        room = serializer.save(owner=request.user, category=category)
                        amenities = request.data.get("amenities")
                        for amenity_id in amenities:
                            amenity = Amenity.objects.get(pk=amenity_id)
                            room.amenities.add(amenity)
                        return Response(RoomDetailSerializer(room).data)
                except Exception:
                    raise ParseError("Amenity not found.")
            else:
                return Response(serializer.errors)
        else:
            raise NotAuthenticated


class RoomDetail(APIView):

    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        room = self.get_object(pk)
        return Response(
            RoomDetailSerializer(
                room,
                context={"request": request},
            ).data
        )

    def put(self, request, pk):
        room = self.get_object(pk)
        if not request.user.is_authenticated:
            raise NotAuthenticated()
        if room.owner != request.user:
            raise PermissionDenied()

        serializer = RoomDetailSerializer(room, data=request.data, partial=True)

        if serializer.is_valid():

            category_id = request.data.get("category")
            if category_id:
                try:
                    category = Category.objects.get(pk=category_id)
                    if category.kind == Category.CategoryKindChoices.EXPERIENCES:
                        raise ParseError("The category kind should be 'rooms'.")
                except Category.DoesNotExist:
                    raise ParseError("Category not found.")

            try:
                with transaction.atomic():
                    room = (
                        serializer.save(category=category)
                        if category_id
                        else serializer.save()
                    )
                    amenities = request.data.get("amenities")

                    if amenities:
                        room.amenities.clear()
                        for amenity_id in amenities:
                            amenity = Amenity.objects.get(pk=amenity_id)
                            room.amenities.add(amenity)

                    return Response(RoomDetailSerializer(room).data)

            except Exception:
                raise ParseError("Amenity not found.")

        else:
            return Response(serializer.errors)

    def delete(self, request, pk):
        room = self.get_object(pk)
        if not request.user.is_authenticated:
            raise NotAuthenticated()
        if room.owner != request.user:
            raise PermissionDenied()
        room.delete()
        return Response(status=HTTP_204_NO_CONTENT)


class RoomReviews(APIView):

    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        try:
            page = int(request.query_params.get("page", 1))
        except ValueError:
            page = 1
        page_size = settings.PAGE_SIZE
        start = (page - 1) * page_size
        end = start + page_size
        room = self.get_object(pk)
        serializer = ReviewSerializer(room.reviews.all()[start:end], many=True)
        return Response(serializer.data)


class RoomPhotos(APIView):
    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound

    def post(self, request, pk):
        room = self.get_object(pk)
        if not request.user.is_authenticated:
            raise NotAuthenticated
        if request.user != room.owner:
            raise PermissionDenied
        serializer = PhotoSerializer(data=request.data)
        if serializer.is_valid():
            photo = serializer.save(room=room)
            serializer = PhotoSerializer(photo)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class RoomAmenities(APIView):

    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        try:
            page = int(request.query_params.get("page", 1))
        except ValueError:
            page = 1

        room = self.get_object(pk)
        page_size = settings.PAGE_SIZE
        start = (page - 1) * page_size
        end = start + page_size
        serializer = AmenitySerializer(room.amenities.all()[start:end], many=True)
        return Response(serializer.data)


class Amenities(APIView):

    def get(self, request):
        all_amenities = Amenity.objects.all()
        serializer = AmenitySerializer(
            all_amenities,
            many=True,
        )
        return Response(serializer.data)

    def post(self, request):
        serializer = AmenitySerializer(data=request.data)
        if serializer.is_valid():
            amenity = serializer.save()
            return Response(AmenitySerializer(amenity).data)
        else:
            return Response(serializer.errors)


class AmenityDetail(APIView):

    def get_object(self, pk):
        try:
            amenity = Amenity.objects.get(pk=pk)
        except Amenity.DoesNotExist:
            raise NotFound
        return amenity

    def get(self, request, pk):
        return Response(AmenitySerializer(self.get_object(pk)).data)

    def put(self, request, pk):
        amenity = self.get_object(pk)
        serializer = AmenitySerializer(
            amenity,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            updated_amenity = serializer.save()
            return Response(AmenitySerializer(updated_amenity).data)
        else:
            return Response(serializer.errors)

    def delete(self, request, pk):
        amenity = self.get_object(pk)
        amenity.delete()
        return Response(status=HTTP_204_NO_CONTENT)
