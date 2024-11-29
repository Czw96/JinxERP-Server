from django_tenants.models import TenantMixin, DomainMixin
from django.db.models import Model
from django.db import models


class Tenant(TenantMixin):
    number = models.CharField(max_length=20, unique=True, verbose_name='编号')
    expiry_time = models.DateTimeField(verbose_name='到期时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='修改时间')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    auto_drop_schema = True
    auto_create_schema = True


class Domain(DomainMixin):
    pass


class ErrorLog(Model):
    """错误日志"""

    module = models.CharField(max_length=20, null=True, blank=True, verbose_name='模块')
    content = models.TextField(null=True, blank=True, verbose_name='内容')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')


__all__ = [
    'Tenant',
    'Domain',
    'ErrorLog',
]
