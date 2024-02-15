# DRF Imports
from rest_framework.serializers import ModelSerializer

# Serializer Imports
from rooms.serializers import RoomListSerializer

# Model Imports
from .models import Wishlist


class RoomsWishlistSerializer(ModelSerializer):

    rooms = RoomListSerializer(read_only=True, many=True)

    class Meta:
        model = Wishlist
        fields = (
            "name",
            "rooms",
        )
