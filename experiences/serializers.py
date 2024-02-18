# DRF Imports
from rest_framework.serializers import ModelSerializer

# Model Imports
from .models import Perk, Experience


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


class PerkSerializer(ModelSerializer):

    class Meta:
        model = Perk
        fields = "__all__"
