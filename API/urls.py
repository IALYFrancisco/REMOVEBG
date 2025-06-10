from django.urls import path
from .views import Index

urlpatterns = [
    path('removebg/', Index, name="RemoveBackground")
]