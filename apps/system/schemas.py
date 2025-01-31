from rest_framework.serializers import Serializer
from rest_framework import serializers


class CreateTokenRequest(Serializer):
    username = serializers.CharField(label='用户名')
    password = serializers.CharField(label='密码')


class CreateTokenResponse(Serializer):
    access = serializers.CharField(label='访问令牌')
    refresh = serializers.CharField(label='刷新令牌')


class UpdateTokenRequest(Serializer):
    refresh = serializers.CharField(label='刷新令牌')


class UpdateTokenResponse(Serializer):
    access = serializers.CharField(label='访问令牌')
    refresh = serializers.CharField(label='刷新令牌')


class RevokeTokenRequest(Serializer):
    refresh = serializers.CharField(label='刷新令牌')


class UserProfileResponse(Serializer):
    id = serializers.IntegerField(label='用户ID')
    number = serializers.CharField(label='编号')
    name = serializers.CharField(label='名称')
    is_manager = serializers.BooleanField(label='管理员状态')
    permissions = serializers.JSONField(label='权限')


class SetPasswordRequest(Serializer):
    old_password = serializers.CharField(label='旧密码')
    new_password = serializers.CharField(label='新密码')


class FieldConfigResponse(Serializer):
    id = serializers.IntegerField(label='字段ID')
    number = serializers.CharField(label='编号')
    name = serializers.CharField(label='名称')
    code = serializers.CharField(label='代码')
    model = serializers.CharField(label='模型')
    type = serializers.CharField(label='类型')
    priority = serializers.IntegerField(label='排序')
    property = serializers.JSONField(label='属性')
    source = serializers.BooleanField(label='来源')


__all__ = [
    'CreateTokenRequest',
    'CreateTokenResponse',
    'UpdateTokenRequest',
    'UpdateTokenResponse',
    'RevokeTokenRequest',
    'UserProfileResponse',
    'SetPasswordRequest',
    'FieldConfigResponse',
]
