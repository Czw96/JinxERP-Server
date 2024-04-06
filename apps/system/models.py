from django.db.models import Model
from django.db import models


class Team(Model):
    number = models.CharField(max_length=32, unique=True, verbose_name='编号')
    expiry_time = models.DateTimeField(verbose_name='到期时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='修改时间')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')


class PagePermission(Model):
    """页面权限"""

    name = models.CharField(max_length=64, verbose_name='名称')
    permissions = models.JSONField(default=list, verbose_name='权限')


class ErrorLog(Model):
    """错误日志"""

    content = models.TextField(verbose_name='内容')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')


__all__ = [
    'Team',
    'PagePermission',
    'ErrorLog',
]
