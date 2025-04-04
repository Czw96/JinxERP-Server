"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import debug_toolbar
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    path('__debug__/', include(debug_toolbar.urls)),

    *static(settings.STATIC_URL, document_root=settings.STATIC_ROOT),
    *static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),

    path('api/', include('apps.tenant.urls')),
    path('api/', include('apps.system.urls')),
    path('api/', include('apps.data.urls')),
    path('api/', include('apps.product.urls')),
    # path('api/', include('apps.approval.urls')),
    # path('api/', include('apps.purchase.urls')),
    # path('api/', include('apps.sales.urls')),
    # path('api/', include('apps.stock_in.urls')),
    # path('api/', include('apps.stock_out.urls')),
    # path('api/', include('apps.stock_count.urls')),
    # path('api/', include('apps.stock_transfer.urls')),
    # path('api/', include('apps.finance.urls')),
    # path('api/', include('apps.flow.urls')),
    # path('api/', include('apps.report.urls')),
    # path('api/', include('apps.stats.urls')),
    path('api/', include('apps.task.urls')),
    path('api/', include('apps.option.urls')),
]
