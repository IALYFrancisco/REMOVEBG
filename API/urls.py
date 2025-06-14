from django.urls import path
from .views import V1, V2

urlpatterns = [
    path('v1', V1.as_view(), name="RemoveBackgroundV1"),
    path('v2', V2.as_view(), name="RemoveBackgroundV2")
]