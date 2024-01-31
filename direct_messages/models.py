from django.db import models
from common.models import CommonModel

# Create your models here.


class ChattingRoom(CommonModel):

    """Chatting Room Model Definition"""

    users = models.ManyToManyField(
        "users.User",
    )

    def __str__(self) -> str:
        return "Chatting Room"


class Message(CommonModel):

    """Message Model Definition"""

    text = models.TextField()
    user = models.ForeignKey(
        "users.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    room = models.ForeignKey(
        "direct_messages.ChattingRoom",
        on_delete=models.CASCADE,
    )

    def __str__(self) -> str:
        return "%s: %s" % (self.user, self.text)
