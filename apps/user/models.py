from django.db.models import Model
from django.db import models

from extensions.models import RefModel


class Role(Model):
    """角色"""

    name = models.CharField(max_length=60, unique=True, verbose_name='名称', error_messages={'unique': '名称已存在'})
    remark = models.CharField(max_length=240, null=True, blank=True, verbose_name='备注')
    permissions = models.JSONField(default=list, verbose_name='权限')
    update_time = models.DateTimeField(auto_now=True, db_index=True, verbose_name='修改时间')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')


class User(RefModel):
    """用户"""

    number = models.CharField(max_length=20, unique=True, verbose_name='编号', error_messages={'unique': '编号已存在'})
    username = models.CharField(max_length=20, verbose_name='用户名')
    password = models.CharField(max_length=120, verbose_name='密码')
    name = models.CharField(max_length=60, verbose_name='名称')
    phone = models.CharField(max_length=20, null=True, blank=True, verbose_name='手机号')
    warehouse_set = models.ManyToManyField('user.Warehouse', blank=True, related_name='user_set', verbose_name='仓库')
    role_set = models.ManyToManyField('user.Role', blank=True, related_name='user_set', verbose_name='角色')
    permissions = models.JSONField(default=list, verbose_name='权限')
    remark = models.CharField(max_length=240, null=True, blank=True, verbose_name='备注')
    is_manager = models.BooleanField(default=False, verbose_name='管理员状态')
    is_active = models.BooleanField(default=True, db_index=True, verbose_name='激活状态')
    update_time = models.DateTimeField(auto_now=True, db_index=True, verbose_name='修改时间')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        unique_together = [('username', 'delete_time'), ('name', 'delete_time')]

    def get_warehouse_set(self):
        if self.is_manager:
            return Warehouse.objects.all()
        return self.warehouse_set.all()


class Warehouse(RefModel):
    """仓库"""

    number = models.CharField(max_length=20, unique=True, verbose_name='编号', error_messages={'unique': '编号已存在'})
    name = models.CharField(max_length=60, verbose_name='名称')
    address = models.CharField(max_length=240, null=True, blank=True, verbose_name='地址')
    remark = models.CharField(max_length=240, null=True, blank=True, verbose_name='备注')
    is_locked = models.BooleanField(default=False, db_index=True, verbose_name='锁定状态')
    is_active = models.BooleanField(default=True, db_index=True, verbose_name='激活状态')
    update_time = models.DateTimeField(auto_now=True, db_index=True, verbose_name='修改时间')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        unique_together = [('name', 'delete_time')]


class Notification(Model):
    """通知"""


__all__ = [
    'Role',
    'User',
    'Warehouse',
    'Notification',
]
