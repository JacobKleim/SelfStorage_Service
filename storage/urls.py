from django.urls import path
from django.shortcuts import render

from . import views


urlpatterns = [
    path('', render, kwargs={'template_name': 'index.html'}, name='start_page'),
    path('boxes/', views.view_products, name='box_page'),
    path('register/', views.register_user, name='register'),
    path('login/', views.login_user, name='login'),
    path('my_rent/', views.my_rent, name='my_rent'),
]
