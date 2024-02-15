# DRF Imports
from rest_framework.serializers import ModelSerializer

# Model Imports
from .models import Booking


class PublicBookingSerializer(ModelSerializer):

    class Meta:
        model = Booking
        fields = (
            "pk",
            "kind",
            "check_in",
            "check_out",
            "experience_time",
            "guests",
        )
