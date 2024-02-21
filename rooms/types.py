import typing
from django.conf import settings
import strawberry
from strawberry import auto

from users.types import UserType
from reviews.types import ReviewType
from . import models


@strawberry.django.type(models.Room)
class RoomType:
    id: auto
    name: auto
    kind: auto
    owner: "UserType"

    @strawberry.field
    def reviews(self, page: int) -> typing.List["ReviewType"]:
        pageSize = settings.PAGE_SIZE
        start = (page - 1) * pageSize
        end = start + pageSize
        return self.reviews.all()[start:end]

    @strawberry.field
    def rating(self) -> str:
        return self.rating()
