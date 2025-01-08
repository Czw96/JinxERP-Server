from rest_framework.serializers import Serializer
from rest_framework import serializers
from django.utils import timezone
from datetime import datetime

from extensions.exceptions import ValidationError
from apps.system.models import ModelField


class TextFieldProperty(Serializer):
    """文本字段"""

    required = serializers.BooleanField(default=False, label='必填状态')
    max_length = serializers.IntegerField(default=60, allow_null=True, min_value=10, max_value=240, label='最大长度')
    default_value = serializers.CharField(default=None, allow_null=True, allow_blank=True, max_length=240, label='默认值')

    def validate(self, attrs):
        max_length = attrs['max_length']
        default_value = attrs['default_value']

        # 验证 max_length, default_value 之间的大小关系
        if default_value is not None and len(default_value) > max_length:
            raise ValidationError('默认值长度不能大于最大长度')

        return super().validate(attrs)

    @classmethod
    def validate_data(cls, model_field, value):
        if isinstance(value, (str, None)):
            raise ValidationError(f'{model_field.name} 类型错误')

        required = model_field.property['required']
        if required and value == None:
            raise ValidationError(f'{model_field.name} 不能为空')

        default_value = model_field.property['default_value']
        if value == None:
            return default_value

        max_length = model_field.property['max_length']
        if len(value) > max_length:
            raise ValidationError(f'{model_field.name} 长度不能大于 {max_length}')

        return value


class NumberFieldProperty(Serializer):
    """数字字段"""

    required = serializers.BooleanField(default=False, label='必填状态')
    precision = serializers.IntegerField(default=None, allow_null=True, min_value=0, label='数值精度')
    min_value = serializers.FloatField(default=None, allow_null=True, label='最小值')
    max_value = serializers.FloatField(default=None, allow_null=True, label='最大值')
    default_value = serializers.FloatField(default=None, allow_null=True, label='默认值')

    def validate(self, attrs):
        min_value = attrs['min_value']
        max_value = attrs['max_value']
        default_value = attrs['default_value']

        # 验证 min_value, max_value, default_value 之间的大小关系
        if min_value is not None and max_value is not None and min_value > max_value:
            raise ValidationError('最小值不能大于最大值')
        if min_value is not None and default_value is not None and min_value > default_value:
            raise ValidationError('默认值不能小于最小值')
        if max_value is not None and default_value is not None and max_value < default_value:
            raise ValidationError('默认值不能大于最大值')

        return super().validate(attrs)

    @classmethod
    def validate_data(cls, model_field, value):
        if isinstance(value, (int, float, None)):
            raise ValidationError(f'{model_field.name} 类型错误')

        required = model_field.property['required']
        if required and value == None:
            raise ValidationError(f'{model_field.name} 不能为空')

        default_value = model_field.property['default_value']
        if value == None:
            return default_value

        precision = model_field.property['precision']
        if value != round(value, precision):
            raise ValidationError(f'{model_field.name} 精度不符合要求')

        min_value = model_field.property['min_value']
        if min_value is not None and value < min_value:
            raise ValidationError(f'{model_field.name} 不能小于 {min_value}')

        max_value = model_field.property['max_value']
        if max_value is not None and value > max_value:
            raise ValidationError(f'{model_field.name} 不能大于 {max_value}')

        return value


class DateFieldProperty(Serializer):
    """日期字段"""

    required = serializers.BooleanField(default=False, label='必填状态')
    default_value = serializers.BooleanField(default=False, label='默认今日')

    @classmethod
    def validate_data(cls, model_field, value):
        if isinstance(value, (str, None)):
            raise ValidationError(f'{model_field.name} 类型错误')

        required = model_field.property['required']
        if required and value == None:
            raise ValidationError(f'{model_field.name} 不能为空')

        default_value = model_field.property['default_value']
        if value == None and default_value:
            return timezone.localtime().strftime('%Y-%m-%d')

        try:
            if value != None:
                datetime.strptime(value, '%Y-%m-%d')
        except ValueError:
            raise ValidationError(f'{model_field.name} 日期格式错误')

        return value


class TimeFieldProperty(Serializer):
    """时间字段"""

    required = serializers.BooleanField(default=False, label='必填状态')
    default_value = serializers.BooleanField(default=False, allow_null=True, label='默认此刻')

    @classmethod
    def validate_data(cls, model_field, value):
        if isinstance(value, (str, None)):
            raise ValidationError(f'{model_field.name} 类型错误')

        required = model_field.property['required']
        if required and value == None:
            raise ValidationError(f'{model_field.name} 不能为空')

        default_value = model_field.property['default_value']
        if value == None and default_value:
            return timezone.localtime().strftime('%H:%M')

        try:
            if value != None:
                datetime.strptime(value, '%H:%M')
        except ValueError:
            raise ValidationError(f'{model_field.name} 时间格式错误')

        return value


class SingleChoiceFieldProperty(Serializer):
    """单选字段"""

    class ChoiceOptionItem(serializers.Serializer):

        label = serializers.CharField(max_length=20, label='选项标签')
        is_default = serializers.BooleanField(default=False, label='默认状态')

    required = serializers.BooleanField(default=False, label='必填状态')
    option_items = serializers.ListField(child=ChoiceOptionItem(), allow_empty=False, max_length=10, label='选项列表')

    def validate(self, attrs):
        option_items = attrs['option_items']

        default_count = sum(1 for item in option_items if item['is_default'])
        if default_count > 1:
            raise ValidationError('存在多个默认选项')

        label_set = {item['label'] for item in option_items}
        if len(label_set) != len(option_items):
            raise ValidationError('存在重复选项')

        return super().validate(attrs)

    @classmethod
    def validate_data(cls, model_field, value):
        if isinstance(value, (str, None)):
            raise ValidationError(f'{model_field.name} 类型错误')

        required = model_field.property['required']
        if required and value == None:
            raise ValidationError(f'{model_field.name} 不能为空')

        option_items = model_field.property['option_items']
        if value == None:
            return next((item['label'] for item in option_items if item['is_default']), None)

        label_set = {item['label'] for item in option_items}
        if value not in label_set:
            raise ValidationError(f'{model_field.name} 选项错误, 不在有效的选项中')

        return value


class MultipleChoiceFieldProperty(Serializer):
    """多选字段"""

    class ChoiceOptionItem(serializers.Serializer):

        label = serializers.CharField(max_length=20, label='选项标签')
        is_default = serializers.BooleanField(default=False, label='默认状态')

    required = serializers.BooleanField(default=False, label='必填状态')
    option_items = serializers.ListField(child=ChoiceOptionItem(), allow_empty=False, max_length=10, label='选项列表')

    def validate(self, attrs):
        option_items = attrs['option_items']

        default_count = sum(1 for item in option_items if item['is_default'])
        if default_count > 1:
            raise ValidationError('存在多个默认选项')

        label_set = {item['label'] for item in option_items}
        if len(label_set) != len(option_items):
            raise ValidationError('存在重复选项')

        return super().validate(attrs)

    @classmethod
    def validate_data(cls, model_field, value):
        if isinstance(value, (list, None)):
            raise ValidationError(f'{model_field.name} 类型错误')

        required = model_field.property['required']
        if required and (value == None or len(value) == 0):
            raise ValidationError(f'{model_field.name} 不能为空')

        option_items = model_field.property['option_items']
        if value == None or len(value) == 0:
            return [item['label'] for item in option_items if item['is_default']]

        label_set = {item['label'] for item in option_items}
        for label in value:
            if label not in label_set:
                raise ValidationError(f'{model_field.name} 选项错误, 不在有效的选项中')

        return value


def validate_extension_data(model, data):
    for model_field in ModelField.objects.filter(model=model, is_deleted=False):
        field_number = model_field.number
        field_value = data.get(field_number, None)
        if model_field.type == ModelField.DataType.TEXT:
            data[field_number] = TextFieldProperty.validate_data(model_field, field_value)
        elif model_field.type == ModelField.DataType.NUMBER:
            data[field_number] = NumberFieldProperty.validate_data(model_field, field_value)
        elif model_field.type == ModelField.DataType.DATE:
            data[field_number] = DateFieldProperty.validate_data(model_field, field_value)
        elif model_field.type == ModelField.DataType.TIME:
            data[field_number] = TimeFieldProperty.validate_data(model_field, field_value)
        elif model_field.type == ModelField.DataType.SINGLE_CHOICE:
            data[field_number] = SingleChoiceFieldProperty.validate_data(model_field, field_value)
        elif model_field.type == ModelField.DataType.MULTIPLE_CHOICE:
            data[field_number] = MultipleChoiceFieldProperty.validate_data(model_field, field_value)
    return data


__all__ = [
    'TextFieldProperty',
    'NumberFieldProperty',
    'DateFieldProperty',
    'TimeFieldProperty',
    'SingleChoiceFieldProperty',
    'MultipleChoiceFieldProperty',
    'validate_extension_data',
]
