from django.db import models

# Create your models here.


class CommonModel(models.Model):
    """
    Common Model Definition
    """

    class Meta:
        abstract = True

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
