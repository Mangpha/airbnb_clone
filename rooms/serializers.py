# DRF Import
from rest_framework.serializers import ModelSerializer, SerializerMethodField

# Model Import
from .models import Amenity, Room

# Serializers Import
from users.serializers import TinyUserSerializer
from categories.serializers import CategorySerializer
from medias.serializers import PhotoSerializer


class AmenitySerializer(ModelSerializer):

    class Meta:
        model = Amenity
        fields = (
            "name",
            "description",
        )


class RoomDetailSerializer(ModelSerializer):

    class Meta:
        model = Room
        fields = "__all__"

    owner = TinyUserSerializer(read_only=True)
    amenities = AmenitySerializer(read_only=True, many=True)
    category = CategorySerializer(read_only=True)
    photos = PhotoSerializer(read_only=True, many=True)

    rating = SerializerMethodField()
    is_owner = SerializerMethodField()

    def get_rating(self, room):
        print(self.context)
        return room.rating()

    def get_is_owner(self, room):
        request = self.context["request"]
        return room.owner == request.user


class RoomListSerializer(ModelSerializer):

    class Meta:
        model = Room
        fields = (
            "pk",
            "name",
            "country",
            "city",
            "price",
            "photos",
            "rating",
            "is_owner",
        )

    photos = PhotoSerializer(read_only=True, many=True)

    rating = SerializerMethodField()
    is_owner = SerializerMethodField()

    def get_rating(self, room):
        return room.rating()

    def get_is_owner(self, room):
        request = self.context["request"]
        return room.owner == request.user
