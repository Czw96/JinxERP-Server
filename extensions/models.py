from typing import Tuple

from django.db import models
from django.db.models import Manager, Model, QuerySet, UniqueConstraint
from django.utils import timezone


class ArchiveQuerySet(QuerySet):

    def delete(self) -> int:
        return self.filter(is_deleted=False).update(is_deleted=True, delete_time=timezone.now())


class ArchiveManager(Manager):

    def get_queryset(self) -> ArchiveQuerySet:
        return ArchiveQuerySet(self.model, using=self._db)


class ArchiveModel(Model):
    is_deleted = models.BooleanField(default=False, db_index=True, verbose_name='删除状态')
    delete_time = models.DateTimeField(null=True, db_index=True, verbose_name='删除时间')

    objects: ArchiveManager = ArchiveManager()

    class Meta:
        abstract = True

    def delete(self, using=None, keep_parents=False) -> Tuple[int, dict[str, int]]:
        if not self.is_deleted:
            self.is_deleted = True
            self.delete_time = timezone.now()
            self.save(update_fields=['is_deleted', 'delete_time'])
        return (0, {})

    def undo_delete(self):
        if self.is_deleted:
            self.is_deleted = False
            self.delete_time = None
            self.save(update_fields=['is_deleted', 'delete_time'])


class UniqueConstraintEx(UniqueConstraint):

    def __init__(
        self,
        *expressions,
        fields=(),
        name=None,
        condition=None,
        deferrable=None,
        include=None,
        opclasses=(),
        nulls_distinct=False,
        violation_error_code=None,
        violation_error_message=None,
    ):
        super().__init__(
            *expressions,
            fields=fields,
            name=name,
            condition=condition,
            deferrable=deferrable,
            include=include,
            opclasses=opclasses,
            nulls_distinct=nulls_distinct,
            violation_error_code=violation_error_code,
            violation_error_message=violation_error_message,
        )


__all__ = [
    'ArchiveModel',
    'UniqueConstraintEx',
]
