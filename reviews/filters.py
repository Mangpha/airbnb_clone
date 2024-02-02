from typing import Any
from django.contrib import admin
from django.db.models.query import QuerySet


class WordFilter(admin.SimpleListFilter):
    title = "Filter by words"

    parameter_name = "word"

    def lookups(self, request: Any, model_admin: Any) -> list[tuple[Any, str]]:
        return [
            ("good", "Good"),
            ("great", "Great"),
            ("awesome", "Awesome"),
        ]

    def queryset(self, request: Any, reviews: QuerySet[Any]) -> QuerySet[Any] | None:
        return (
            reviews.filter(payload__contains=self.value()) if self.value() else reviews
        )


class RatingFilter(admin.SimpleListFilter):
    title = "Filter by rating"

    parameter_name = "rating"

    def lookups(self, request: Any, model_admin: Any) -> list[tuple[Any, str]]:
        return [(4, "Good"), (3, "Ordinary"), (2, "Bad")]

    def queryset(self, request: Any, reviews: QuerySet[Any]) -> QuerySet[Any] | None:
        try:
            rating = int(self.value())
            if rating == 4:
                return reviews.filter(rating__gte=rating)
            elif rating == 3:
                return reviews.filter(rating__exact=rating)
            elif rating == 2:
                return reviews.filter(rating__lte=rating)
            else:
                return reviews
        except (ValueError, TypeError):
            return reviews
