from datetime import datetime

from rest_framework import serializers
from rest_framework.serializers import Serializer

from apps.system.models import ModelField
from extensions.exceptions import ValidationError


class TextFieldProperty(Serializer):
    """文本字段"""

    required = serializers.BooleanField(label='必填状态')
    max_length = serializers.IntegerField(min_value=10, max_value=240, label='最大长度')
    default_value = serializers.CharField(default=None, allow_null=True, allow_blank=True, label='默认值')

    def validate(self, attrs):
        max_length = attrs['max_length']
        default_value = attrs['default_value']

        # 验证 max_length, default_value 之间的大小关系
        if default_value != None and len(default_value) > max_length:
            raise ValidationError('默认值长度不能大于最大长度')

        return super().validate(attrs)

    @classmethod
    def validate_data(cls, model_field, value):
        if value is None:
            if model_field.property['required']:
                raise ValidationError(f'{model_field.name} 不能为空')
            return None

        if not isinstance(value, str):
            raise ValidationError(f'{model_field.name} 类型错误')

        max_length = model_field.property['max_length']
        if len(value) > max_length:
            raise ValidationError(f'{model_field.name} 长度不能大于 {max_length}')

        return value


class NumberFieldProperty(Serializer):
    """数字字段"""

    required = serializers.BooleanField(label='必填状态')
    precision = serializers.IntegerField(min_value=0, label='数值精度')
    min_value = serializers.FloatField(default=None, allow_null=True, label='最小值')
    max_value = serializers.FloatField(default=None, allow_null=True, label='最大值')
    default_value = serializers.FloatField(default=None, allow_null=True, label='默认值')

    def validate(self, attrs):
        precision = attrs['precision']
        min_value = attrs['min_value']
        max_value = attrs['max_value']
        default_value = attrs['default_value']

        # 验证 min_value, max_value, default_value 之间的大小关系
        if min_value != None and max_value != None and min_value > max_value:
            raise ValidationError('最小值不能大于最大值')
        if min_value != None and default_value != None and min_value > default_value:
            raise ValidationError('默认值不能小于最小值')
        if max_value != None and default_value != None and max_value < default_value:
            raise ValidationError('默认值不能大于最大值')

        # 验证 precision, default_value
        if default_value != None and default_value != round(default_value, precision):
            raise ValidationError(f'默认值精度不符合要求')

        return super().validate(attrs)

    @classmethod
    def validate_data(cls, model_field, value):
        if value is None:
            if model_field.property['required']:
                raise ValidationError(f'{model_field.name} 不能为空')
            return None

        if not isinstance(value, (int, float)):
            raise ValidationError(f'{model_field.name} 类型错误')

        precision = model_field.property['precision']
        if value != round(value, precision):
            raise ValidationError(f'{model_field.name} 精度不符合要求')

        min_value = model_field.property['min_value']
        if min_value != None and value < min_value:
            raise ValidationError(f'{model_field.name} 不能小于 {min_value}')

        max_value = model_field.property['max_value']
        if max_value != None and value > max_value:
            raise ValidationError(f'{model_field.name} 不能大于 {max_value}')

        return value


class BooleanFieldProperty(Serializer):
    """布尔字段"""

    required = serializers.BooleanField(label='必填状态')
    true_label = serializers.CharField(max_length=20, label='真值标签')
    false_label = serializers.CharField(max_length=20, label='假值标签')
    default_value = serializers.BooleanField(default=None, allow_null=True, label='默认值')

    @classmethod
    def validate_data(cls, model_field, value):
        if value is None:
            if model_field.property['required']:
                raise ValidationError(f'{model_field.name} 不能为空')
            return None

        if not isinstance(value, bool):
            raise ValidationError(f'{model_field.name} 类型错误')

        return value


class DateFieldProperty(Serializer):
    """日期字段"""

    required = serializers.BooleanField(label='必填状态')
    default_value = serializers.BooleanField(default=False, label='默认今日')

    @classmethod
    def validate_data(cls, model_field, value):
        if value is None:
            if model_field.property['required']:
                raise ValidationError(f'{model_field.name} 不能为空')
            return None

        if not isinstance(value, str):
            raise ValidationError(f'{model_field.name} 类型错误')

        try:
            datetime.strptime(value, '%Y-%m-%d')
        except ValueError:
            raise ValidationError(f'{model_field.name} 日期格式错误')

        return value


class TimeFieldProperty(Serializer):
    """时间字段"""

    required = serializers.BooleanField(label='必填状态')
    default_value = serializers.BooleanField(default=False, allow_null=True, label='默认此刻')

    @classmethod
    def validate_data(cls, model_field, value):
        if value is None:
            if model_field.property['required']:
                raise ValidationError(f'{model_field.name} 不能为空')
            return None

        if not isinstance(value, str):
            raise ValidationError(f'{model_field.name} 类型错误')

        try:
            datetime.strptime(value, '%H:%M')
        except ValueError:
            raise ValidationError(f'{model_field.name} 时间格式错误')

        return value


class ListFieldProperty(Serializer):
    """列表字段"""

    required = serializers.BooleanField(label='必填状态')
    max_length = serializers.IntegerField(min_value=0, max_value=10, label='最大长度')
    default_value = serializers.ListField(
        child=serializers.CharField(max_length=60, label='项'), allow_empty=True, max_length=10, label='默认值')

    def validate(self, attrs):
        max_length = attrs['max_length']
        default_value = attrs['default_value']

        # 验证 max_length, default_value 之间的大小关系
        if len(default_value) > max_length:
            raise ValidationError('默认值长度不能大于最大长度')

        return super().validate(attrs)

    @classmethod
    def validate_data(cls, model_field, value):
        if not isinstance(value, list):
            raise ValidationError(f'{model_field.name} 类型错误')

        if len(value) == 0:
            if model_field.property['required']:
                raise ValidationError(f'{model_field.name} 不能为空')
            return None

        max_length = model_field.property['max_length']
        if len(value) > max_length:
            raise ValidationError(f'{model_field.name} 长度不能大于 {max_length}')

        for _value in value:
            if len(_value) > 60:
                raise ValidationError(f'{model_field.name} 每项长度不能大于 60')

        return value


class SingleChoiceFieldProperty(Serializer):
    """单选字段"""

    required = serializers.BooleanField(label='必填状态')
    option_list = serializers.ListField(
        child=serializers.CharField(max_length=60, label='选项标签'), max_length=10, allow_empty=False, label='选项列表')
    default_value = serializers.CharField(default=None, allow_null=True, max_length=60, label='默认值')

    def validate(self, attrs):
        option_list = attrs['option_list']
        option_set = set(option_list)
        if len(option_set) != len(option_list):
            raise ValidationError('存在重复选项')

        default_value = attrs['default_value']
        if default_value != None and default_value not in option_set:
            raise ValidationError(f'默认值[{default_value}] 不在选项列表中')

        return super().validate(attrs)

    @classmethod
    def validate_data(cls, model_field, value):
        if value is None:
            if model_field.property['required']:
                raise ValidationError(f'{model_field.name} 不能为空')
            return None

        if not isinstance(value, str):
            raise ValidationError(f'{model_field.name} 类型错误')

        option_list = model_field.property['option_list']
        if value not in option_list:
            raise ValidationError(f'{model_field.name} 选项错误, {value} 不在有效的选项中')

        return value


class MultipleChoiceFieldProperty(Serializer):
    """多选字段"""

    required = serializers.BooleanField(label='必填状态')
    option_list = serializers.ListField(
        child=serializers.CharField(max_length=60, label='选项标签'), max_length=10, allow_empty=False, label='选项列表')
    default_value = serializers.ListField(
        child=serializers.CharField(max_length=60, label='项'), allow_empty=True, max_length=10, label='默认值')

    def validate(self, attrs):
        option_list = attrs['option_list']
        option_set = set(option_list)
        if len(option_set) != len(option_list):
            raise ValidationError('存在重复选项')

        default_value = attrs['default_value']
        for value in default_value:
            if value not in option_set:
                raise ValidationError(f'默认值[{value}] 不在选项列表中')

        return super().validate(attrs)

    @classmethod
    def validate_data(cls, model_field, value):
        if not isinstance(value, list):
            raise ValidationError(f'{model_field.name} 类型错误')

        if len(value) == 0:
            if model_field.property['required']:
                raise ValidationError(f'{model_field.name} 不能为空')
            return None

        option_list = model_field.property['option_list']
        not_in_option_list = [option for option in value if option not in option_list]
        if len(not_in_option_list) > 0:
            raise ValidationError(f'{model_field.name} 选项错误, 选项{not_in_option_list} 不在有效的选项中')

        return value


def validate_custom_data(model, data):
    for model_field in ModelField.objects.filter(model=model, is_deleted=False):
        field_number = model_field.number
        field_value = data.get(field_number, None)
        if model_field.type == ModelField.DataType.TEXT:
            data[field_number] = TextFieldProperty.validate_data(model_field, field_value)
        elif model_field.type == ModelField.DataType.NUMBER:
            data[field_number] = NumberFieldProperty.validate_data(model_field, field_value)
        elif model_field.type == ModelField.DataType.BOOLEAN:
            data[field_number] = BooleanFieldProperty.validate_data(model_field, field_value)
        elif model_field.type == ModelField.DataType.DATE:
            data[field_number] = DateFieldProperty.validate_data(model_field, field_value)
        elif model_field.type == ModelField.DataType.TIME:
            data[field_number] = TimeFieldProperty.validate_data(model_field, field_value)
        elif model_field.type == ModelField.DataType.LIST:
            data[field_number] = ListFieldProperty.validate_data(model_field, field_value)
        elif model_field.type == ModelField.DataType.SINGLE_CHOICE:
            data[field_number] = SingleChoiceFieldProperty.validate_data(model_field, field_value)
        elif model_field.type == ModelField.DataType.MULTIPLE_CHOICE:
            data[field_number] = MultipleChoiceFieldProperty.validate_data(model_field, field_value)
    return data


def export_extension_data(model, data):
    model_field_set = ModelField.objects.filter(model=model, is_deleted=False).order_by('-priority')

    extension_item = {}
    for model_field in model_field_set:
        if model_field.type == ModelField.DataType.TEXT:
            extension_item[model_field.name] = data.get(model_field.number, None)
        elif model_field.type == ModelField.DataType.NUMBER:
            extension_item[model_field.name] = data.get(model_field.number, None)
        elif model_field.type == ModelField.DataType.BOOLEAN:
            value = data.get(model_field.number, None)
            if value == True:
                extension_item[model_field.name] = model_field.property['true_label']
            elif value == False:
                extension_item[model_field.name] = model_field.property['false_label']
            else:
                extension_item[model_field.name] = None
        elif model_field.type == ModelField.DataType.DATE:
            extension_item[model_field.name] = data.get(model_field.number, None)
        elif model_field.type == ModelField.DataType.TIME:
            extension_item[model_field.name] = data.get(model_field.number, None)
        elif model_field.type == ModelField.DataType.LIST:
            value = data.get(model_field.number, [])
            extension_item[model_field.name] = ';'.join(value)
        elif model_field.type == ModelField.DataType.SINGLE_CHOICE:
            value = data.get(model_field.number, None)
        elif model_field.type == ModelField.DataType.MULTIPLE_CHOICE:
            value = data.get(model_field.number, [])
            extension_item[model_field.name] = ';'.join(value)
    return extension_item


__all__ = [
    'TextFieldProperty',
    'NumberFieldProperty',
    'BooleanFieldProperty',
    'DateFieldProperty',
    'TimeFieldProperty',
    'ListFieldProperty',
    'SingleChoiceFieldProperty',
    'MultipleChoiceFieldProperty',
    'validate_custom_data',
    'export_extension_data',
]
