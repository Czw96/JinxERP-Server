from rest_framework.validators import UniqueTogetherValidator, qs_exists
from rest_framework.serializers import ModelSerializer
from rest_framework.exceptions import ValidationError


class ModelSerializerEx(ModelSerializer):

    @property
    def request(self):
        return self.context['request']

    @property
    def user(self):
        return self.context['request'].user


class UniqueTogetherValidatorEX(UniqueTogetherValidator):

    def __init__(self, fields, message=None):
        self.queryset = None
        self.fields = fields
        self.message = message or self.message

    def __call__(self, attrs, serializer):
        self.enforce_required_fields(attrs, serializer)
        queryset = serializer.Meta.model.objects.all()
        queryset = self.filter_queryset(attrs, queryset, serializer)
        queryset = self.exclude_current_instance(attrs, queryset, serializer.instance)

        # Ignore validation if any field is None
        if serializer.instance is None:
            checked_values = [
                value for field, value in attrs.items() if field in self.fields
            ]
        else:
            # Ignore validation if all field values are unchanged
            checked_values = [
                value
                for field, value in attrs.items()
                if field in self.fields and value != getattr(serializer.instance, field)
            ]

        if checked_values and None not in checked_values and qs_exists(queryset):
            field_names = ', '.join(self.fields)
            message = self.message.format(field_names=field_names)
            raise ValidationError(message, code='unique')


__all__ = [
    'ModelSerializerEx',
    'UniqueTogetherValidatorEX',
]
