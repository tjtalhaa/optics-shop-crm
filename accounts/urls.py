from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    # home
    path('', views.home, name="home"),

    # user-register-auth
    path('register/', views.registerPage, name="register"),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),

    # orders pages with admin access
    path('orders_pannel', views.ordersPannel, name='orders_pannel'),


    # product
    path('productsC/', views.productsC, name='productsC'),
    path('products/', views.products, name='products'),
    path('add_product/', views.addProduct, name="add_product"),
    path('update_product/<str:pk>/', views.updateProduct, name="update_product"),
    path('delete_product/<str:pk>/', views.deleteProduct, name="delete_product"),

    # user(customer) dashboard and settingspage
    path('user/', views.userPage, name="user-page"),
    path('account/', views.accountSettings, name="account"),

    # customer pannel but (admin access)
    path('customer/<str:pk_test>/', views.customer, name="customer"),
    path('create_order/<str:pk>/', views.createOrder, name="create_order"),
    path('update_order/<str:pk>/', views.updateOrder, name="update_order"),
    path('delete_order/<str:pk>/', views.deleteOrder, name="delete_order"),

    # password-reset-email
    path('reset_password/',
         auth_views.PasswordResetView.as_view(
             template_name="userauth/password_reset.html"),
         name="reset_password"),

    path('reset_password_sent/',
         auth_views.PasswordResetDoneView.as_view(
             template_name="userauth/password_reset_sent.html"),
         name="password_reset_done"),

    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name="userauth/password_reset_form.html"),
         name="password_reset_confirm"),

    path('reset_password_complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name="userauth/password_reset_done.html"),
         name="password_reset_complete"),



]
