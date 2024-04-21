from django.urls import path, include


urlpatterns = [
    path('v1/logs/', include("apps.log_aggregator.api.v1.urls"))
]