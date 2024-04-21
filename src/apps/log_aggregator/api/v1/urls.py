from django.urls import path, include

from rest_framework.routers import DefaultRouter

from apps.log_aggregator.api.v1.views import NginxLogEntryViewSet

router = DefaultRouter()
router.register(r'nginx-logs', NginxLogEntryViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
