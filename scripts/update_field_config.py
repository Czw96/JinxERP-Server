from django_tenants.utils import tenant_context
from django.db import transaction

from apps.tenant.models import Tenant
from apps.system.models import User


def run(*args):
    ...
