from datetime import timedelta

from django.contrib.auth.hashers import make_password
from django.db import transaction
from django.utils import timezone
from django_tenants.utils import tenant_context

from apps.system.models import User
from apps.tenant.models import Domain, Tenant


def run():
    register_number = input('注册ID: ')
    domain_name = input('域名: ')
    username = input('用户名: ')
    activation_days = input('激活天数: ')
    expiry_time = timezone.now() + timedelta(days=float(activation_days))

    with transaction.atomic():
        tenant = Tenant.objects.create(number=register_number, schema_name=register_number, expiry_time=expiry_time)
        Domain.objects.create(domain=domain_name, tenant=tenant)

        with tenant_context(tenant):
            User.objects.create(
                number="U001", username=username, password=make_password(username), name=username, is_manager=True)
