from typing import Tuple
from django.db.models import Model, Manager, QuerySet, UniqueConstraint
from django.db import models
from django.utils import timezone


class SoftDeleteQuerySet(QuerySet):

    def delete(self) -> int:
        return self.filter(is_deleted=False).update(is_deleted=True, delete_time=timezone.now())


class SoftDeleteManager(Manager):

    def get_queryset(self) -> SoftDeleteQuerySet:
        return SoftDeleteQuerySet(self.model, using=self._db)

    def all(self) -> SoftDeleteQuerySet:
        return super().filter(is_deleted=False)

    def filter(self, *args, **kwargs) -> SoftDeleteQuerySet:
        return super().filter(is_deleted=False).filter(*args, **kwargs)

    def exclude(self, *args, **kwargs) -> SoftDeleteQuerySet:
        return super().filter(is_deleted=False).exclude(*args, **kwargs)

    def all_with_deleted(self) -> SoftDeleteQuerySet:
        return super().all()


class SoftDeleteMixin(Model):
    is_deleted = models.BooleanField(default=False, db_index=True, verbose_name='删除状态')
    delete_time = models.DateTimeField(null=True, verbose_name='删除时间')

    objects = SoftDeleteManager()

    def delete(self, using=None, keep_parents=False) -> Tuple[int, dict[str, int]]:
        if not self.is_deleted:
            self.is_deleted = True
            self.delete_time = timezone.now()
            self.save(update_fields=['is_deleted', 'delete_time'])
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
    'SoftDeleteMixin',
    'UniqueConstraintEx',
]
