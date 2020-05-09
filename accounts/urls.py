from django.urls import path
from . import views


urlpatterns = [
    path('', views.home,  name='home'),
    path('customer/<str:pk>/', views.customer,  name='customer'),

    path('products/', views.products, name='product'),

    path('create_order/<str:pk>/', views.create_order, name='create_order'),
    path('update_order/<str:pk>/', views.update_order,  name='update_order'),
    path('delete_order/<str:pk>/', views.delete_order,  name='delete_order'),

    path('register/', views.registerpage,  name='register'),
    path('login/', views.loginpage,  name='login'),
    path('logout/', views.logoutuser,  name='logout'),
]
