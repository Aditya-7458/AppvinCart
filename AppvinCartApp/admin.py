from django.contrib import admin

from .models import Products

# Register your models here.
@ admin.register (Products)
class ProductsAdmin(admin.ModelAdmin):
    list_display=['name','image','price','stock_available']


