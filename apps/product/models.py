from django.db.models import Model
from django.db import models

from extensions.models import SoftDeleteMixin, UniqueConstraintEx


class Product(SoftDeleteMixin, Model):
    """产品"""

    number = models.CharField(max_length=20, unique=True, verbose_name='编号', error_messages={'unique': '编号已存在'})
    name = models.CharField(max_length=120, db_index=True, verbose_name='名称')
    barcode = models.CharField(max_length=20, db_index=True, verbose_name='条码')
    spec = models.CharField(max_length=60, null=True, blank=True, verbose_name='规格')
    category = models.ForeignKey(
        'data.ProductCategory', on_delete=models.SET_NULL, null=True, related_name='product_set', verbose_name='产品分类')
    main_image = models.ForeignKey(
        'product.ProductImage', on_delete=models.SET_NULL, null=True, related_name='product_set', verbose_name='主图')
    brand = models.ForeignKey(
        'data.Brand', on_delete=models.SET_NULL, null=True, related_name='product_set', verbose_name='品牌')
    unit = models.CharField(max_length=20, null=True, blank=True, verbose_name='单位')
    remark = models.CharField(max_length=240, null=True, blank=True, verbose_name='备注')
    is_active = models.BooleanField(default=True, db_index=True, verbose_name='激活状态')

    supplier_set = models.ManyToManyField('data.Supplier', blank=True, related_name='product_set', verbose_name='供应商')
    enable_batch_control = models.BooleanField(default=False, db_index=True, verbose_name='批次控制')
    expiration_days = models.IntegerField(null=True, verbose_name='有效期天数')
    expiration_warning_days = models.IntegerField(null=True, verbose_name='有效期预警天数')
    extension_data = models.JSONField(default=dict, verbose_name='扩展数据')
    update_time = models.DateTimeField(auto_now=True, db_index=True, verbose_name='修改时间')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    is_deleted = models.BooleanField(default=False, db_index=True, verbose_name='删除状态')
    delete_time = models.DateTimeField(null=True, verbose_name='删除时间')

    class Meta:
        constraints = [
            UniqueConstraintEx(fields=['name', 'spec', 'delete_time'], name='product'),
        ]


class ProductImage(Model):
    """产品图片"""

    product = models.ForeignKey(
        'product.Product', on_delete=models.CASCADE, null=True, related_name='product_image_set', verbose_name='产品')
    file = models.ImageField(upload_to='product_images', verbose_name='文件')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')


class Inventory(Model):
    """库存"""

    warehouse = models.ForeignKey(
        'system.Warehouse', on_delete=models.CASCADE, related_name='inventory_set', verbose_name='仓库')
    product = models.ForeignKey(
        'product.Product', on_delete=models.CASCADE, related_name='inventory_set', verbose_name='产品')
    purchase_price = models.FloatField(null=True, verbose_name='采购单价')
    sales_price = models.FloatField(null=True, verbose_name='销售单价')
    level_price1 = models.FloatField(null=True, verbose_name='等级价一')
    level_price2 = models.FloatField(null=True, verbose_name='等级价二')
    level_price3 = models.FloatField(null=True, verbose_name='等级价三')
    total_quantity = models.FloatField(default=0, db_index=True, verbose_name='库存数量')
    has_stock = models.BooleanField(default=False, db_index=True, verbose_name='库存状态')
    is_on_sale = models.BooleanField(default=True, db_index=True, verbose_name='在售状态')
    enable_warning = models.BooleanField(default=False, db_index=True, verbose_name='预警启用状态')
    min_quantity = models.FloatField(null=True, verbose_name='最小数量')
    max_quantity = models.FloatField(null=True, verbose_name='最大数量')

    class Meta:
        constraints = [
            UniqueConstraintEx(fields=['warehouse', 'product'], name='inventory'),
        ]


class Batch(Model):
    """批次"""

    number = models.CharField(max_length=20, db_index=True, verbose_name='编号')
    inventory = models.ForeignKey(
        'product.Inventory', on_delete=models.CASCADE, related_name='batch_set', verbose_name='库存')
    warehouse = models.ForeignKey(
        'system.Warehouse', on_delete=models.CASCADE, related_name='batch_set', verbose_name='仓库')
    product = models.ForeignKey(
        'product.Product', on_delete=models.CASCADE, related_name='batch_set', verbose_name='产品')
    total_quantity = models.FloatField(default=0, db_index=True, verbose_name='库存数量')
    has_stock = models.BooleanField(default=False, db_index=True, verbose_name='库存状态')
    production_date = models.DateField(null=True, db_index=True, verbose_name='生产日期')
    warning_date = models.DateField(null=True, db_index=True, verbose_name='预警日期')
    expiry_date = models.DateField(null=True, db_index=True, verbose_name='到期日期')
    remark = models.CharField(max_length=240, null=True, blank=True, verbose_name='备注')

    class Meta:
        constraints = [
            UniqueConstraintEx(fields=['number', 'inventory', 'production_date'], name='batch'),
        ]


__all__ = [
    'Product',
    'ProductImage',
    'Inventory',
    'Batch',
]
