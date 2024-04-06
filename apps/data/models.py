from django.db.models import Model
from django.db import models

from extensions.choices import ClientLevel
from extensions.models import RefModel


class Account(RefModel):
    """账户"""

    number = models.CharField(max_length=32, verbose_name='编号')
    name = models.CharField(max_length=64, verbose_name='名称')
    code = models.CharField(max_length=64, null=True, blank=True, verbose_name='代码')
    remark = models.CharField(max_length=256, null=True, blank=True, verbose_name='备注')
    is_active = models.BooleanField(default=True, verbose_name='激活状态')

    initial_balance_amount = models.DecimalField(default=0, max_digits=12, decimal_places=2, verbose_name='初期余额')
    balance_amount = models.DecimalField(default=0, max_digits=12, decimal_places=2, verbose_name='余额')
    update_time = models.DateTimeField(auto_now=True, verbose_name='修改时间')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    team = models.ForeignKey('system.Team', on_delete=models.CASCADE, related_name='account_set')

    class Meta:
        unique_together = [('number', 'team'), ('name', 'delete_time', 'team')]


class SupplierCategory(Model):
    """供应商分类"""

    name = models.CharField(max_length=64, verbose_name='名称')
    code = models.CharField(max_length=64, null=True, blank=True, verbose_name='代码')
    remark = models.CharField(max_length=256, null=True, blank=True, verbose_name='备注')
    parent = models.ForeignKey(
        'data.SupplierCategory', on_delete=models.CASCADE, null=True, related_name='supplier_category_set', verbose_name='父级')
    is_parent = models.BooleanField(default=True, verbose_name='父级状态')
    update_time = models.DateTimeField(auto_now=True, verbose_name='修改时间')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    team = models.ForeignKey('system.Team', on_delete=models.CASCADE, related_name='supplier_category_set')

    class Meta:
        unique_together = [('name', 'team')]


class Supplier(RefModel):
    """供应商"""

    number = models.CharField(max_length=32, verbose_name='编号')
    name = models.CharField(max_length=64, verbose_name='名称')
    code = models.CharField(max_length=64, null=True, blank=True, verbose_name='代码')
    category_set = models.ManyToManyField(
        'data.SupplierCategory', blank=True, related_name='supplier_set', verbose_name='供应商分类')
    contact = models.CharField(max_length=64, null=True, blank=True, verbose_name='联系人')
    phone = models.CharField(max_length=32, null=True, blank=True, verbose_name='手机号')
    address = models.CharField(max_length=256, null=True, blank=True, verbose_name='地址')
    remark = models.CharField(max_length=256, null=True, blank=True, verbose_name='备注')
    is_active = models.BooleanField(default=True, verbose_name='激活状态')

    initial_arrears_amount = models.DecimalField(default=0, max_digits=12, decimal_places=2, verbose_name='初期欠款金额')
    arrears_amount = models.DecimalField(default=0, max_digits=12, decimal_places=2, verbose_name='欠款金额')
    update_time = models.DateTimeField(auto_now=True, verbose_name='修改时间')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    team = models.ForeignKey('system.Team', on_delete=models.CASCADE, related_name='supplier_set')

    class Meta:
        unique_together = [('number', 'team'), ('name', 'delete_time', 'team')]


class ClientCategory(Model):
    """客户分类"""

    name = models.CharField(max_length=64, verbose_name='名称')
    code = models.CharField(max_length=64, null=True, blank=True, verbose_name='代码')
    remark = models.CharField(max_length=256, null=True, blank=True, verbose_name='备注')
    parent = models.ForeignKey(
        'data.ClientCategory', on_delete=models.CASCADE, null=True, related_name='client_category_set', verbose_name='父级')
    is_parent = models.BooleanField(default=True, verbose_name='父级状态')
    update_time = models.DateTimeField(auto_now=True, verbose_name='修改时间')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    team = models.ForeignKey('system.Team', on_delete=models.CASCADE, related_name='client_category_set')

    class Meta:
        unique_together = [('name', 'team')]


class Client(RefModel):
    """客户"""

    number = models.CharField(max_length=32, verbose_name='编号')
    name = models.CharField(max_length=64, verbose_name='名称')
    code = models.CharField(max_length=64, null=True, blank=True, verbose_name='代码')
    category_set = models.ManyToManyField(
        'data.ClientCategory', blank=True, related_name='supplier_set', verbose_name='客户分类')
    level = models.CharField(max_length=32, choices=ClientLevel.choices, default=ClientLevel.LEVEL0, verbose_name='客户等级')
    contact = models.CharField(max_length=64, null=True, blank=True, verbose_name='联系人')
    phone = models.CharField(max_length=32, null=True, blank=True, verbose_name='手机号')
    address = models.CharField(max_length=256, null=True, blank=True, verbose_name='地址')
    remark = models.CharField(max_length=256, null=True, blank=True, verbose_name='备注')
    is_active = models.BooleanField(default=True, verbose_name='激活状态')

    initial_arrears_amount = models.DecimalField(default=0, max_digits=12, decimal_places=2, verbose_name='初期欠款金额')
    arrears_amount = models.DecimalField(default=0, max_digits=12, decimal_places=2, verbose_name='欠款金额')
    update_time = models.DateTimeField(auto_now=True, verbose_name='修改时间')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    team = models.ForeignKey('system.Team', on_delete=models.CASCADE, related_name='client_set')

    class Meta:
        unique_together = [('number', 'team'), ('name', 'delete_time', 'team')]


class ProductCategory(Model):
    """产品分类"""

    name = models.CharField(max_length=64, verbose_name='名称')
    code = models.CharField(max_length=64, null=True, blank=True, verbose_name='代码')
    remark = models.CharField(max_length=256, null=True, blank=True, verbose_name='备注')
    parent = models.ForeignKey(
        'data.ProductCategory', on_delete=models.CASCADE, null=True, related_name='product_category_set', verbose_name='父级')
    is_parent = models.BooleanField(default=True, verbose_name='父级状态')
    update_time = models.DateTimeField(auto_now=True, verbose_name='修改时间')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    team = models.ForeignKey('system.Team', on_delete=models.CASCADE, related_name='product_category_set')

    class Meta:
        unique_together = [('name', 'team')]


class Brand(Model):
    """品牌"""

    name = models.CharField(max_length=64, verbose_name='名称')
    code = models.CharField(max_length=64, null=True, blank=True, verbose_name='代码')
    remark = models.CharField(max_length=256, null=True, blank=True, verbose_name='备注')
    update_time = models.DateTimeField(auto_now=True, verbose_name='修改时间')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    team = models.ForeignKey('system.Team', on_delete=models.CASCADE, related_name='brand_set')

    class Meta:
        unique_together = [('name', 'team')]


class Unit(Model):
    """单位"""

    name = models.CharField(max_length=64, verbose_name='名称')
    code = models.CharField(max_length=64, null=True, blank=True, verbose_name='代码')
    remark = models.CharField(max_length=256, null=True, blank=True, verbose_name='备注')
    update_time = models.DateTimeField(auto_now=True, verbose_name='修改时间')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    team = models.ForeignKey('system.Team', on_delete=models.CASCADE, related_name='unit_set')

    class Meta:
        unique_together = [('name', 'team')]


class ChargeCategory(Model):
    """收支分类"""

    name = models.CharField(max_length=64, verbose_name='名称')
    code = models.CharField(max_length=64, null=True, blank=True, verbose_name='代码')
    remark = models.CharField(max_length=256, null=True, blank=True, verbose_name='备注')
    parent = models.ForeignKey(
        'data.ChargeCategory', on_delete=models.CASCADE, null=True, related_name='charge_category_set', verbose_name='父级')
    is_parent = models.BooleanField(default=True, verbose_name='父级状态')
    update_time = models.DateTimeField(auto_now=True, verbose_name='修改时间')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    team = models.ForeignKey('system.Team', on_delete=models. CASCADE, related_name='charge_category_set')

    class Meta:
        unique_together = [('name', 'team')]


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
