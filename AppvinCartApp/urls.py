from django.contrib import admin
from django.urls import path,include
from .import views
from rest_framework_simplejwt.views import TokenVerifyView


from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)



urlpatterns = [
   
    path('',views.Home,name='Home'),
    path('cart',views.Cart,name='Cart'),
    path('orders',views.Orders,name='Orders'),
    path('profile',views.Profile,name='Profile'),
    path('signup',views.SignUp,name='SignUp'),
    path('login',views.LogIn,name='LogIn'),
    path('logout',views.LogOut,name='LogOut'),
    path('forgot_password', views.forgotPassword,name='forgotPassword'),
    path('reset_password',views.resetPassword,name='resetPassword'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify')

]
