from django.contrib import admin
from .models import Review
from .filters import WordFilter, RatingFilter

# Register your models here.


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        "__str__",
        "payload",
    )

    list_filter = (
        WordFilter,
        RatingFilter,
        "rating",
        "user__is_host",
    )
