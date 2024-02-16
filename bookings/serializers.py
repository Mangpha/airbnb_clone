# Django Imports
from django.utils import timezone

# DRF Imports
from rest_framework.serializers import ModelSerializer, DateField, ValidationError

# Model Imports
from .models import Booking


class CreateRoomBookingSerializer(ModelSerializer):

    check_in = DateField()
    check_out = DateField()

    class Meta:
        model = Booking
        fields = (
            "check_in",
            "check_out",
            "guests",
        )

    def validate_check_in(self, value):
        now = timezone.localtime(timezone.now()).date()
        if now > value:
            raise ValidationError("Can't book in the past.")
        return value

    def validate_check_out(self, value):
        now = timezone.localtime(timezone.now()).date()
        if now > value:
            raise ValidationError("Can't book in the past.")
        return value

    def validate(self, data):
        if data["check_in"] >= data["check_out"]:
            raise ValidationError("Check in should be smaller than check out.")
        if Booking.objects.filter(
            check_in__lte=data["check_out"],
            check_out__gte=data["check_in"],
        ).exists():
            raise ValidationError("Those (or some) of those dates are already taken.")
        return data


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
