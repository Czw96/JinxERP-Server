from django.contrib.auth.hashers import make_password
from django.utils import timezone
from django.db import transaction
from datetime import timedelta

from scripts.Permissions import PERMISSIONS
from apps.system.models import *


def run(*args):
    number = input('注册ID: ')
    username = input('用户名: ')
    activation_days = input('激活天数: ')
    expiry_time = timezone.now() + timedelta(days=float(activation_days))

    with transaction.atomic():
        team = Team.objects.create(number=number, expiry_time=expiry_time)
        warehouse = Warehouse.objects.create(number='W001', name='默认仓库', team=team)
        user = User.objects.create(
            username=username, password=make_password(username), name=username, code=username, is_manager=True, team=team)
        user.warehouse_set.add(warehouse)

        PagePermission.objects.bulk_create(
            [PagePermission(name=item['name'], permissions=item['permissions']) for item in PERMISSIONS])
