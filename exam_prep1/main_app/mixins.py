from django.db import models


class Mixin(models.Model):
    is_awarded = models.BooleanField(default=False)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
