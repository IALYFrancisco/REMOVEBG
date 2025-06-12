from django.urls import path
from .views import V5

urlpatterns = [
    path('v5', V5.as_view(), name="RemoveBackground")
]