from django.urls import path, include
from django.contrib import admin

from config.redoc import schema_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('apps.log_aggregator.api.urls')),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

]
