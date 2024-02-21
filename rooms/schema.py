import strawberry
import typing
from rooms.queries import get_all_rooms
from rooms.types import RoomType


@strawberry.type
class Query:
    all_rooms: typing.List[RoomType] = strawberry.field(resolver=get_all_rooms)
