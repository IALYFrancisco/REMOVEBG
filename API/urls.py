from django.urls import path
from .views import Index

urlpatterns = [
    path('v5', Index.as_view(), name="RemoveBackground")
]