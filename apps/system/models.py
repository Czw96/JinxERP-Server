from django.db.models import Model
from django.db import models

from extensions.models import ArchiveModel, UniqueConstraintEx


class Role(Model):
    """角色"""

    name = models.CharField(max_length=60, db_index=True, verbose_name='名称')
    remark = models.CharField(max_length=240, null=True, blank=True, verbose_name='备注')
    permissions = models.JSONField(default=list, verbose_name='权限')
    extension_data = models.JSONField(default=dict, verbose_name='扩展数据')
    update_time = models.DateTimeField(auto_now=True, db_index=True, verbose_name='修改时间')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')


class User(ArchiveModel):
    """用户"""

    number = models.CharField(max_length=20, unique=True, verbose_name='编号')
    username = models.CharField(max_length=20, verbose_name='用户名')
    password = models.CharField(max_length=120, verbose_name='密码')
    name = models.CharField(max_length=60, verbose_name='名称')
    phone = models.CharField(max_length=20, null=True, blank=True, verbose_name='手机号')
    warehouse_set = models.ManyToManyField('system.Warehouse', blank=True, related_name='user_set', verbose_name='仓库')
    role_set = models.ManyToManyField('system.Role', blank=True, related_name='user_set', verbose_name='角色')
    permissions = models.JSONField(default=list, verbose_name='权限')
    remark = models.CharField(max_length=240, null=True, blank=True, verbose_name='备注')
    is_manager = models.BooleanField(default=False, verbose_name='管理员状态')
    is_active = models.BooleanField(default=True, db_index=True, verbose_name='激活状态')
    extension_data = models.JSONField(default=dict, verbose_name='扩展数据')
    update_time = models.DateTimeField(auto_now=True, db_index=True, verbose_name='修改时间')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    is_deleted = models.BooleanField(default=False, db_index=True, verbose_name='删除状态')
    delete_time = models.DateTimeField(null=True, db_index=True, verbose_name='删除时间')

    class Meta:
        constraints = [
            UniqueConstraintEx(fields=['username', 'delete_time'], name='User.unique_username'),
            UniqueConstraintEx(fields=['name', 'delete_time'], name='User.unique_name'),
        ]

    def get_warehouse_set(self):
        if self.is_manager:
            return Warehouse.objects.filter(is_deleted=False)
        return self.warehouse_set.filter(is_deleted=False)


class Warehouse(ArchiveModel):
    """仓库"""

    number = models.CharField(max_length=20, unique=True, verbose_name='编号')
    name = models.CharField(max_length=60, verbose_name='名称')
    address = models.CharField(max_length=240, null=True, blank=True, verbose_name='地址')
    remark = models.CharField(max_length=240, null=True, blank=True, verbose_name='备注')
    is_locked = models.BooleanField(default=False, db_index=True, verbose_name='锁定状态')
    is_active = models.BooleanField(default=True, db_index=True, verbose_name='激活状态')
    extension_data = models.JSONField(default=dict, verbose_name='扩展数据')
    update_time = models.DateTimeField(auto_now=True, db_index=True, verbose_name='修改时间')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    is_deleted = models.BooleanField(default=False, db_index=True, verbose_name='删除状态')
    delete_time = models.DateTimeField(null=True, db_index=True, verbose_name='删除时间')

    class Meta:
        constraints = [
            UniqueConstraintEx(fields=['name', 'delete_time'], name='Warehouse.unique_name'),
        ]


class ModelField(ArchiveModel):
    """模型字段"""

    class DataModel(models.TextChoices):
        """数据模型"""

        ROLE = ('role', '角色权限')
        USER = ('user', '员工账号')
        WAREHOUSE = ('warehouse', '仓库管理')
        ACCOUNT = ('account', '结算账户')

    class DataType(models.TextChoices):
        """数据类型"""

        TEXT = ('text', '文本')
        NUMBER = ('number', '数字')
        DATE = ('date', '日期')
        TIME = ('time', '时间')
        SINGLE_CHOICE = ('single_choice', '单选')
        MULTIPLE_CHOICE = ('multiple_choice', '多选')

    number = models.CharField(max_length=20, unique=True, verbose_name='编号')
    name = models.CharField(max_length=60, verbose_name='名称')
    model = models.CharField(max_length=20, choices=DataModel, db_index=True, verbose_name='模型')
    type = models.CharField(max_length=20, choices=DataType, verbose_name='类型')
    priority = models.IntegerField(default=0, verbose_name='排序')
    remark = models.CharField(max_length=240, null=True, blank=True, verbose_name='备注')
    property = models.JSONField(default=dict, verbose_name='属性')
    update_time = models.DateTimeField(auto_now=True, db_index=True, verbose_name='修改时间')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    is_deleted = models.BooleanField(default=False, db_index=True, verbose_name='删除状态')
    delete_time = models.DateTimeField(null=True, db_index=True, verbose_name='删除时间')

    class Meta:
        constraints = [
            UniqueConstraintEx(fields=['name', 'model', 'delete_time'], name='ModelField.unique_name_model'),
        ]


class Notification(Model):
    """通知"""

    class NotificationType(models.TextChoices):
        """通知类型"""

        INFO = ('info', '信息')
        SUCCESS = ('success', '成功')
        WARNING = ('warning', '警告')
        ERROR = ('error', '错误')

    class AttachmentFormat(models.TextChoices):
        """附件格式类型"""

        EXCEL = ('excel', 'Excel 文件')
        PDF = ('pdf', 'PDF 文件')
        IMAGE = ('image', '图片文件')

    title = models.CharField(max_length=20, verbose_name='标题')
    type = models.CharField(max_length=20, choices=NotificationType.choices, verbose_name='通知类型')
    content = models.CharField(max_length=240, verbose_name='内容')
    attachment = models.FileField(null=True, verbose_name='附件')
    attachment_name = models.CharField(max_length=60, null=True, blank=True, verbose_name='附件名称')  
    attachment_format = models.CharField(max_length=20, choices=AttachmentFormat.choices, null=True, verbose_name='附件格式')
    has_attachment = models.BooleanField(default=False, verbose_name='附件状态')
    notifier = models.ForeignKey(
        'system.User', on_delete=models.CASCADE, related_name='notification_set', verbose_name='通知人')
    is_read = models.BooleanField(default=False, db_index=True, verbose_name='已读状态')
    create_time = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='创建时间')


__all__ = [
    'Role',
    'User',
    'Warehouse',
    'ModelField',
    'Notification',
]
