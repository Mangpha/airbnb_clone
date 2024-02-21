import typing
import strawberry
from config.permissions import OnlyLoggedIn

from rooms.queries import get_all_rooms, get_room
from rooms.types import RoomType


@strawberry.type
class Query:
    all_rooms: typing.List[RoomType] = strawberry.field(
        resolver=get_all_rooms, permission_classes=[OnlyLoggedIn]
    )
    room: RoomType = strawberry.field(resolver=get_room)
