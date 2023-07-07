"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from rest_framework import permissions
from rest_framework.schemas import get_schema_view

admin.site.site_header = "MT DATASOURCES ADMIN PANEL"
admin.site.site_title = "MT DATASOURCES MANAGER"
admin.site.index_title = "Admin Home"

urlpatterns = [
    path('api-schema/', get_schema_view(
        title="Your Project",
        description="",
        version="0.1.0",
        urlconf='project.urls',
        permission_classes=(permissions.AllowAny,)
    ), name="openapi-schema"),
    path('redoc/', TemplateView.as_view(
        template_name='redoc.html',
        extra_context={'schema_url':'openapi-schema'}
    ), name='redoc'),
    path('platform-admin/', admin.site.urls),
    path('api/users/login/', TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path('api/users/token/refresh/', TokenRefreshView.as_view(), name="token_refresh"),
    path('api/users/token/verify/', TokenVerifyView.as_view(), name="token_verify"),
    path('api/users/', include('coreauth.urls')),
    path('api/v1/', include('dbanalysis.urls')),
]
