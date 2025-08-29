"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.http import HttpResponsePermanentRedirect
from django.urls import path, include, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.views.decorators.csrf import csrf_exempt
from api.views import health as api_health

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    # Project-level health to make liveness checks easy at /health
    path('health/', api_health, name='root-health'),
]

schema_view = get_schema_view(
   openapi.Info(
      title="My API",
      default_version='v1',
      description="Test description",
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

def get_full_url(request):
    scheme = request.scheme
    host = request.get_host()
    forwarded_port = request.META.get("HTTP_X_FORWARDED_PORT")

    if ':' not in host and forwarded_port:
        host = f"{host}:{forwarded_port}"

    return f"{scheme}://{host}"

@csrf_exempt
def dynamic_schema_view(request, *args, **kwargs):
    url = get_full_url(request)
    view = get_schema_view(
        openapi.Info(
            title="My API",
            default_version='v1',
            description="API Docs",
        ),
        public=True,
        url=url,
    )
    return view.with_ui('swagger', cache_timeout=0)(request)

# Redirect root "/" to docs UI, so preview shows API docs by default.
def root_redirect(request):
    return HttpResponsePermanentRedirect('/docs/')

urlpatterns += [
    path('', root_redirect, name='root'),
    re_path(r'^docs/$', dynamic_schema_view, name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    re_path(r'^swagger\.json$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
]