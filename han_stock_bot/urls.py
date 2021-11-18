from django.urls import path
from . import views

urlpatterns = [
    path('line_callback', views.line_callback)
]