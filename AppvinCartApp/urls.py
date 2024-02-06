from django.contrib import admin
from django.urls import path,include
from .import views

urlpatterns = [
   
    path('',views.Home,name='Home'),
    path('cart',views.Cart,name='Cart'),
    path('orders',views.Orders,name='Orders'),
    path('profile',views.Profile,name='Profile'),
    path('signup',views.SignUp,name='SignUp'),
    path('login',views.LogIn,name='LogIn'),
    path('logout',views.LogOut,name='LogOut')

]
