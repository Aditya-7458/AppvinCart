from django.contrib import admin

from .models import Products,Users


# Register your models here.
@ admin.register (Products)
class ProductsAdmin(admin.ModelAdmin):
    list_display=['name','image','price','stock_available']

@ admin.register(Users)
class UsersAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email','username' ,'phone','address','gender']

