from django.shortcuts import redirect
from django.urls import path, include
from django.shortcuts import render

from . import views

app_name = "storage"

urlpatterns = [
    path('boxes/', views.view_products, name='box_page'),
]