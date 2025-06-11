from django.urls import path
from .views import Index

urlpatterns = [
    path('removebg', Index.as_view(), name="RemoveBackground")
]