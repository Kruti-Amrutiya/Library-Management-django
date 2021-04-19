from django.db import models


class CustomManager(models.Manager):
    def get_stu_id_range(self, i1, i2):
        return super().get_queryset().filter(id__range=(i1, i2))
