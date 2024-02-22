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
    path('cart',views.view_Cart,name='Cart'),
    path('orders',views.viewOrders,name='viewOrders'),
    path('profile',views.Profile,name='Profile'),
    path('signup',views.SignUp,name='SignUp'),
    path('login',views.LogIn,name='LogIn'),
    path('logout',views.LogOut,name='LogOut'),
    path('forgot_password', views.forgotPassword,name='forgotPassword'),
    path('reset_password',views.resetPassword,name='resetPassword'),


    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),



    path('add_to_cart/<int:productId>/', views.addToCart, name='addToCart'),
    path('cart/update/<int:cart_item_id>/', views.update_cart, name='update_cart'),



    path('buy_now', views.buyNow, name='buyNow'),

    path('place_order',views.placeOrder,name='placeOrder'),
    


    path('success/', views.success_view, name='success_url'),
    path('cancel/', views.cancel_view, name='cancel_url'),



]
