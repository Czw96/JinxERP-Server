from rest_framework.serializers import ModelSerializer


class ModelSerializerEx(ModelSerializer):

    @property
    def request(self):
        return self.context['request']

    @property
    def user(self):
        return self.context['request'].user


__all__ = [
    'ModelSerializerEx',
]
