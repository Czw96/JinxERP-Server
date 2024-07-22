from rest_framework.serializers import Serializer
from rest_framework import serializers


class TextFieldProperty(Serializer):
    """文本字段"""

    required = serializers.BooleanField(default=False, allow_null=True, label='必填状态')
    default_value = serializers.CharField(default=None, allow_null=True, max_length=240, label='默认值')


class NumberFieldProperty(Serializer):
    """数字字段"""

    required = serializers.BooleanField(default=False, allow_null=True, label='必填状态')
    precision = serializers.IntegerField(default=0, allow_null=True, min_value=0, label='数值精度')
    min_value = serializers.FloatField(default=None, allow_null=True, label='最小值')
    max_value = serializers.FloatField(default=None, allow_null=True, label='最大值')
    default_value = serializers.FloatField(default=None, allow_null=True, label='默认值')

    def validate(self, attrs):
        min_value = attrs['min_value']
        max_value = attrs['max_value']
        default_value = attrs['default_value']

        # 验证 min_value, max_value, default_value 之间的大小关系
        if min_value is not None and max_value is not None and min_value > max_value:
            raise serializers.ValidationError({'min_value': '最小值不能大于最大值'})
        if min_value is not None and default_value is not None and min_value > default_value:
            raise serializers.ValidationError({'default_value': '默认值不能小于最小值'})
        if max_value is not None and default_value is not None and max_value < default_value:
            raise serializers.ValidationError({'default_value': '默认值不能大于最大值'})

        return super().validate(attrs)


class DateFieldProperty(Serializer):
    """日期字段"""

    required = serializers.BooleanField(default=False, allow_null=True, label='必填状态')
    default_value = serializers.BooleanField(default=False, allow_null=True, label='默认值')


class TimeFieldProperty(Serializer):
    """时间字段"""

    required = serializers.BooleanField(default=False, allow_null=True, label='必填状态')
    default_value = serializers.BooleanField(default=False, allow_null=True, label='默认值')


class SingleChoiceFieldProperty(Serializer):
    """单选字段"""

    class ChoiceOptionItem(serializers.Serializer):

        id = serializers.CharField(max_length=36, label='选项ID')
        label = serializers.CharField(max_length=20, label='选项标签')
        is_default = serializers.BooleanField(default=False, label='默认状态')

    required = serializers.BooleanField(default=False, allow_null=True, label='必填状态')
    option_items = serializers.ListField(child=ChoiceOptionItem(), allow_empty=False, max_length=10, label='选项列表')


class MultipleChoiceFieldProperty(Serializer):
    """多选字段"""

    class ChoiceOptionItem(serializers.Serializer):

        id = serializers.CharField(max_length=36, label='选项ID')
        label = serializers.CharField(max_length=20, label='选项标签')
        is_default = serializers.BooleanField(default=False, label='默认状态')

    required = serializers.BooleanField(default=False, allow_null=True, label='必填状态')
    option_items = serializers.ListField(child=ChoiceOptionItem(), allow_empty=False, max_length=10, label='选项列表')


__all__ = [
    'TextFieldProperty',
    'NumberFieldProperty',
    'DateFieldProperty',
    'TimeFieldProperty',
    'SingleChoiceFieldProperty',
    'MultipleChoiceFieldProperty',
]
