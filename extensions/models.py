
from django.db.models import Model, Manager, QuerySet
from django.db import models
from django.utils import timezone
from typing import Dict, Tuple


class RefQuerySet(QuerySet):

    def delete(self) -> Tuple[int, Dict[str, int]]:
        self.filter(is_deleted=False).update(is_deleted=True, delete_time=timezone.now())
        return (0, {})


class RefManager(Manager):

    def get_queryset(self) -> RefQuerySet:
        return RefQuerySet(model=self.model, using=self._db, hints=self._hints)

    def all(self, include_deleted=False) -> RefQuerySet['RefModel']:
        if include_deleted:
            return super().all()
        return super().all().filter(is_deleted=False)

    def filter(self, include_deleted=False, *args, **kwargs) -> RefQuerySet['RefModel']:
        if include_deleted:
            return super().filter(*args, **kwargs)
        return super().filter(*args, **kwargs).filter(is_deleted=False)


class RefModel(Model):
    is_deleted = models.BooleanField(default=False, db_index=True, verbose_name='删除状态')
    delete_time = models.DateTimeField(null=True, verbose_name='删除时间')
    objects: RefManager = RefManager()

    class Meta:
        abstract = True

    def delete(self, using=None, keep_parents=None) -> Tuple[int, Dict[str, int]]:
        if not self.is_deleted:
            self.is_deleted = True
            self.delete_time = timezone.now()
            self.save(update_fields=['is_deleted', 'delete_time'])
        return (0, {})


__all__ = [
    'RefModel',
]
