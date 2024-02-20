# DRF Imports
from rest_framework.serializers import ModelSerializer
from rest_framework import exceptions

# Model Imports
from .models import Perk, Experience

# Serializer Imports
from users.serializers import TinyUserSerializer
from categories.serializers import CategorySerializer


class PerkSerializer(ModelSerializer):

    class Meta:
        model = Perk
        fields = "__all__"


class ExperienceListSerializer(ModelSerializer):

    class Meta:
        model = Experience
        fields = (
            "id",
            "country",
            "city",
            "name",
            "host",
            "price",
            "address",
            "start",
            "end",
        )


class ExperienceDetailSerializer(ModelSerializer):

    class Meta:
        model = Experience
        fields = "__all__"

    host = TinyUserSerializer(read_only=True)
    perks = PerkSerializer(read_only=True, many=True)
    category = CategorySerializer(read_only=True)

    def validate(self, data):
        if data["start"] > data["end"]:
            raise exceptions.ValidationError(
                "Start time should be smaller than End time."
            )
        return data
