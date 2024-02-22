import typing
import strawberry

from rooms.queries import get_all_rooms, get_room
from rooms.types import RoomType


@strawberry.type
class Query:
    all_rooms: typing.List[RoomType] = strawberry.field(
        resolver=get_all_rooms,
    )
    room: RoomType = strawberry.field(resolver=get_room)
