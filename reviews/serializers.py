# DRF Import
from rest_framework import serializers

# Models Import
from .models import Review

# Serializers import
from users.serializers import TinyUserSerializer


class ReviewSerializer(serializers.ModelSerializer):

    user = TinyUserSerializer(read_only=True)

    class Meta:
        model = Review
        fields = (
            "user",
            "payload",
            "rating",
        )
