from django.urls import path
from .views import V2

urlpatterns = [
    path('v5', V2.as_view(), name="RemoveBackground")
]