from rest_framework.serializers import ModelSerializer
from rest_framework.validators import UniqueTogetherValidator
from extensions.exceptions import ValidationError


class ModelSerializerEx(ModelSerializer):

    @property
    def request(self):
        return self.context['request']

    @property
    def user(self):
        return self.context['request'].user

    def validate_unique(self, queryset, fields, message):
        queryset = queryset.filter(**fields)
        if self.instance:
            queryset = queryset.exclude(pk=self.instance.pk)

        if queryset.exists():
            raise ValidationError(message)


class UniqueTogetherValidatorEX(UniqueTogetherValidator):

    def __call__(self, attrs, serializer):
        queryset = self.queryset
        if serializer.instance:
            queryset = queryset.exclude(pk=serializer.instance.pk)

        for field in self.fields:
            queryset = queryset.filter(**{field: attrs.get(field)})

        if queryset.exists():
            raise ValidationError(self.message)


__all__ = [
    'ModelSerializerEx',
    'UniqueTogetherValidatorEX',
]
