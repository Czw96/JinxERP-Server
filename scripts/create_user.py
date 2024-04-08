from django.contrib.auth.hashers import make_password
from django.utils import timezone
from django.db import transaction
from django_tenants.utils import tenant_context
from datetime import timedelta

from apps.system.models import Team, Domain
from apps.user.models import User


def run(*args):
    register_number = input('注册ID: ')
    domain_name = input('域名: ')
    username = input('用户名: ')
    activation_days = input('激活天数: ')
    expiry_time = timezone.now() + timedelta(days=float(activation_days))

    with transaction.atomic():
        team = Team.objects.create(schema_name=register_number, expiry_time=expiry_time)
        Domain.objects.create(domain=domain_name, tenant=team)

        with tenant_context(team):
            User.objects.create(
                username=username, password=make_password(username), name=username, code=username, is_manager=True)
