from django.db import models


class Mixin(models.Model):
    creation_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True
