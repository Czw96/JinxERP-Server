from rest_framework.serializers import Serializer
from rest_framework import serializers


class MakeTokenRequest(Serializer):
    number = serializers.CharField(label='Team 编号')
    username = serializers.CharField(label='用户名')
    password = serializers.CharField(label='密码')


class MakeTokenResponse(Serializer):
    access = serializers.CharField(label='访问令牌')
    refresh = serializers.CharField(label='刷新令牌')


class RefreshTokenRequest(Serializer):
    refresh = serializers.CharField(label='刷新令牌')


class LogoffTokenRequest(Serializer):
    refresh = serializers.CharField(label='刷新令牌')


class RefreshTokenResponse(Serializer):
    access = serializers.CharField(label='访问令牌')
    refresh = serializers.CharField(label='刷新令牌')


class UserInfoResponse(Serializer):
    id = serializers.IntegerField(label='用户ID')
    number = serializers.CharField(label='编号')
    username = serializers.CharField(label='用户名')
    name = serializers.CharField(label='名称')
    is_manager = serializers.BooleanField(label='管理员状态')
    permissions = serializers.JSONField(label='权限')


class SetPasswordRequest(Serializer):
    old_password = serializers.CharField(label='旧密码')
    new_password = serializers.CharField(label='新密码')


__all__ = [
    'MakeTokenRequest',
    'MakeTokenResponse',
    'RefreshTokenRequest',
    'RefreshTokenResponse',
    'LogoffTokenRequest',
    'UserInfoResponse',
    'SetPasswordRequest',
]
