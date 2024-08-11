from typing import Tuple
from django.db.models import Model, Manager, QuerySet, UniqueConstraint
from django.db import models
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

    def delete(self, using=None, keep_parents=False) -> Tuple[int, dict[str, int]]:
        if not self.is_deleted:
            self.is_deleted = True
            self.delete_time = timezone.now()
            self.save()
        return (0, {})

    class Meta:
        abstract = True


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
        if name and 'unique' not in name:
            field_names = '_'.join(fields)
            name = f'{name}_unique_{field_names}'

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
