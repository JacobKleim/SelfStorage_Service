from django.urls import path

from . import views

urlpatterns = [
    path('boxes/', views.view_products, name='box_page'),
    path('register/', views.register_user, name='register'),
    path('login/', views.login_user, name='login'),
    path('my_rent/<int:user_id>/', views.my_rent, name='my_rent'),
    path('count/', views.count, name='rent_count'),
]
