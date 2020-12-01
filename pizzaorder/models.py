import json
from enum import Enum

from django.db import models
# from django.db.models import JSONField
from django.core import serializers
from django.utils.translation import ugettext_lazy

class CoreEnum(Enum):
    @classmethod
    def list(cls):
        return list(map(lambda c: [c.name, c.value], cls))

    @classmethod
    def choose_list(cls):
        return list(
            map(lambda c: [c.value, ugettext_lazy(' '.join(x.capitalize() or '_' for x in c.value.split('_')))], cls))


class CoreModelQuery(models.QuerySet):
    def actives(self):
        return self.filter(is_active=True)


class BaseManager(models.Manager):
    def get_queryset(self):
        return CoreModelQuery(self.model, using=self._db)

    def actives(self):
        return self.get_queryset().actives()


class CoreModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    # created_by = models.ForeignKey(
    #     "auth.User", on_delete=models.PROTECT,
    #     null=True, blank=True,
    #     related_name="%(app_label)s_%(class)s_created_by"
    # )
    is_active = models.BooleanField(default=True)
    # data = JSONField(null=True, blank=True, default=dict)

    objects = BaseManager()

    def __str__(self):
        return str(self.id)

    class Meta:
        abstract = True
        ordering = ["id"]

    def _json(self):
        json_ = json.loads(serializers.serialize("json", [self]))[0]['fields']
        json_.update({
            'id': self.id
        })
        return json_

    def save(self, *args, **kwargs):
        super(CoreModel, self).save(*args, **kwargs)

