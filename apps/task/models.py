from django.db import models
from django.db.models import Model


class ExportTask(Model):
    """导出任务"""

    class DataModel(models.TextChoices):
        """数据模型"""

        ACCOUNT = ('account', '结算账户')

    class ExportStatus(models.TextChoices):
        """导出状态"""

        EXPORTING = ('exporting', '导出中')
        CANCELLED = ('cancelled', '已取消')
        COMPLETED = ('completed', '已完成')
        FAILED = ('failed', '导出失败')

    number = models.CharField(max_length=20, null=True, unique=True, verbose_name='编号')
    model = models.CharField(max_length=20, choices=DataModel.choices, db_index=True, verbose_name='模型')
    export_id_list = models.JSONField(default=list, verbose_name='导出 ID 列表')
    export_file = models.FileField(null=True, verbose_name='导出文件')
    export_count = models.IntegerField(null=True, verbose_name='导出条数')
    status = models.CharField(
        max_length=32, choices=ExportStatus.choices, db_index=True, default=ExportStatus.EXPORTING, verbose_name='导出状态')
    celery_task_number = models.CharField(max_length=60, verbose_name='任务编号')
    error_message = models.TextField(null=True, blank=True, verbose_name='错误信息')
    duration = models.IntegerField(null=True, verbose_name='耗时(秒)')
    creator = models.ForeignKey('system.User', on_delete=models.PROTECT, related_name='export_task_set', verbose_name='创建人')
    create_time = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='创建时间')


class ImportTask(Model):
    """导入记录"""

    class DataModel(models.TextChoices):
        """数据模型"""

        ACCOUNT = ('account', '结算账户')

    class ImportStatus(models.TextChoices):
        """导入状态"""

        IMPORTING = ('importing', '导入中')
        CANCELLED = ('cancelled', '已取消')
        COMPLETED = ('completed', '已完成')
        FAILED = ('failed', '导入失败')

    number = models.CharField(max_length=20, unique=True, verbose_name='编号')
    model = models.CharField(max_length=20, choices=DataModel.choices, db_index=True, verbose_name='模型')
    import_file = models.FileField(verbose_name='导入文件')
    import_count = models.IntegerField(null=True, verbose_name='导入条数')
    status = models.CharField(
        max_length=32, choices=ImportStatus.choices, db_index=True, default=ImportStatus.IMPORTING, verbose_name='导入状态')
    celery_task_number = models.CharField(max_length=60, verbose_name='任务编号')
    error_message_list = models.JSONField(default=list, verbose_name='错误信息')
    duration = models.IntegerField(null=True, verbose_name='耗时(秒)')
    creator = models.ForeignKey('system.User', on_delete=models.PROTECT, related_name='import_task_set', verbose_name='创建人')
    create_time = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='创建时间')


__all__ = [
    'ExportTask',
    'ImportTask',
]
