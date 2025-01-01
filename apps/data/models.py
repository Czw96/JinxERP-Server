from django.db.models import Model
from django.db import models

from extensions.choices import ClientLevel
from extensions.models import ArchiveModel, UniqueConstraintEx


class Account(ArchiveModel):
    """结算账户"""

    number = models.CharField(max_length=20, unique=True, verbose_name='编号')
    name = models.CharField(max_length=60, verbose_name='名称')
    remark = models.CharField(max_length=240, null=True, blank=True, verbose_name='备注')
    is_enabled = models.BooleanField(default=True, db_index=True, verbose_name='启用状态')

    initial_balance_amount = models.DecimalField(default=0, max_digits=12, decimal_places=2, verbose_name='初期余额')
    balance_amount = models.DecimalField(default=0, max_digits=12, decimal_places=2, db_index=True, verbose_name='余额')
    extension_data = models.JSONField(default=dict, verbose_name='扩展数据')
    update_time = models.DateTimeField(auto_now=True, db_index=True, verbose_name='修改时间')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    is_deleted = models.BooleanField(default=False, db_index=True, verbose_name='删除状态')
    delete_time = models.DateTimeField(null=True, db_index=True, verbose_name='删除时间')

    class Meta:
        constraints = [
            UniqueConstraintEx(fields=['name', 'delete_time'], name='Account.unique_name'),
        ]


class SupplierCategory(Model):
    """供应商分类"""

    name = models.CharField(max_length=60, db_index=True, verbose_name='名称')
    remark = models.CharField(max_length=240, null=True, blank=True, verbose_name='备注')
    extension_data = models.JSONField(default=dict, verbose_name='扩展数据')
    update_time = models.DateTimeField(auto_now=True, db_index=True, verbose_name='修改时间')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')


class Supplier(ArchiveModel):
    """供应商"""

    number = models.CharField(max_length=20, unique=True, verbose_name='编号')
    name = models.CharField(max_length=60, verbose_name='名称')
    category = models.ForeignKey(
        'data.SupplierCategory', on_delete=models.SET_NULL, null=True, related_name='supplier_set', verbose_name='供应商分类')
    contact = models.CharField(max_length=60, null=True, blank=True, verbose_name='联系人')
    phone = models.CharField(max_length=20, null=True, blank=True, verbose_name='手机号')
    address = models.CharField(max_length=240, null=True, blank=True, verbose_name='地址')
    remark = models.CharField(max_length=240, null=True, blank=True, verbose_name='备注')
    is_enabled = models.BooleanField(default=True, db_index=True, verbose_name='启用状态')

    initial_arrears_amount = models.DecimalField(default=0, max_digits=12, decimal_places=2, verbose_name='初期欠款金额')
    arrears_amount = models.DecimalField(default=0, max_digits=12, decimal_places=2, db_index=True, verbose_name='欠款金额')
    extension_data = models.JSONField(default=dict, verbose_name='扩展数据')
    update_time = models.DateTimeField(auto_now=True, db_index=True, verbose_name='修改时间')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    is_deleted = models.BooleanField(default=False, db_index=True, verbose_name='删除状态')
    delete_time = models.DateTimeField(null=True, db_index=True, verbose_name='删除时间')

    class Meta:
        constraints = [
            UniqueConstraintEx(fields=['name', 'delete_time'], name='Supplier.unique_name'),
        ]


class ClientCategory(Model):
    """客户分类"""

    name = models.CharField(max_length=60, db_index=True, verbose_name='名称')
    remark = models.CharField(max_length=240, null=True, blank=True, verbose_name='备注')
    extension_data = models.JSONField(default=dict, verbose_name='扩展数据')
    update_time = models.DateTimeField(auto_now=True, db_index=True, verbose_name='修改时间')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')


class Client(ArchiveModel):
    """客户"""

    number = models.CharField(max_length=20, unique=True, verbose_name='编号')
    name = models.CharField(max_length=60, verbose_name='名称')
    category = models.ForeignKey(
        'data.ClientCategory', on_delete=models.SET_NULL, null=True, related_name='supplier_set', verbose_name='客户分类')
    level = models.CharField(
        max_length=20, choices=ClientLevel.choices, default=ClientLevel.LEVEL0, db_index=True, verbose_name='客户等级')
    contact = models.CharField(max_length=60, null=True, blank=True, verbose_name='联系人')
    phone = models.CharField(max_length=20, null=True, blank=True, verbose_name='手机号')
    address = models.CharField(max_length=240, null=True, blank=True, verbose_name='地址')
    remark = models.CharField(max_length=240, null=True, blank=True, verbose_name='备注')
    is_enabled = models.BooleanField(default=True, db_index=True, verbose_name='启用状态')

    initial_arrears_amount = models.DecimalField(default=0, max_digits=12, decimal_places=2, verbose_name='初期欠款金额')
    arrears_amount = models.DecimalField(default=0, max_digits=12, decimal_places=2, db_index=True, verbose_name='欠款金额')
    extension_data = models.JSONField(default=dict, verbose_name='扩展数据')
    update_time = models.DateTimeField(auto_now=True, db_index=True, verbose_name='修改时间')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    is_deleted = models.BooleanField(default=False, db_index=True, verbose_name='删除状态')
    delete_time = models.DateTimeField(null=True, db_index=True, verbose_name='删除时间')

    class Meta:
        constraints = [
            UniqueConstraintEx(fields=['name', 'delete_time'], name='Client.unique_name'),
        ]


class ProductCategory(Model):
    """产品分类"""

    name = models.CharField(max_length=60, db_index=True, verbose_name='名称')
    remark = models.CharField(max_length=240, null=True, blank=True, verbose_name='备注')
    extension_data = models.JSONField(default=dict, verbose_name='扩展数据')
    update_time = models.DateTimeField(auto_now=True, db_index=True, verbose_name='修改时间')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')


class Brand(Model):
    """品牌"""

    name = models.CharField(max_length=60, db_index=True, verbose_name='名称')
    remark = models.CharField(max_length=240, null=True, blank=True, verbose_name='备注')
    extension_data = models.JSONField(default=dict, verbose_name='扩展数据')
    update_time = models.DateTimeField(auto_now=True, db_index=True, verbose_name='修改时间')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')


class Unit(Model):
    """单位"""

    name = models.CharField(max_length=60, db_index=True, verbose_name='名称')
    remark = models.CharField(max_length=240, null=True, blank=True, verbose_name='备注')
    extension_data = models.JSONField(default=dict, verbose_name='扩展数据')
    update_time = models.DateTimeField(auto_now=True, db_index=True, verbose_name='修改时间')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')


class ChargeCategory(Model):
    """收支分类"""

    name = models.CharField(max_length=60, db_index=True, verbose_name='名称')
    remark = models.CharField(max_length=240, null=True, blank=True, verbose_name='备注')
    extension_data = models.JSONField(default=dict, verbose_name='扩展数据')
    update_time = models.DateTimeField(auto_now=True, db_index=True, verbose_name='修改时间')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')


__all__ = [
    'Account',
    'SupplierCategory',
    'Supplier',
    'ClientCategory',
    'Client',
    'ProductCategory',
    'Brand',
    'Unit',
    'ChargeCategory',
]
