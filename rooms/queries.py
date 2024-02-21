from .models import Room


def get_all_rooms():
    return Room.objects.all()


def get_room(id: int):
    return Room.objects.get(pk=id)
