from rest_framework.serializers import ModelSerializer
from extensions.exceptions import ValidationError


class ModelSerializerEx(ModelSerializer):

    @property
    def request(self):
        return self.context['request']

    @property
    def user(self):
        return self.context['request'].user

    def check_unique(self, queryset, fields, message):
        queryset = queryset.filter(**fields)
        if self.instance:
            queryset = queryset.exclude(pk=self.instance.pk)

        if queryset.exists():
            raise ValidationError(message)

    def validate_unique(self, attrs):
        pass

    def validate(self, attrs):
        self.validate_unique(attrs)
        return super().validate(attrs)


__all__ = [
    'ModelSerializerEx',
]
