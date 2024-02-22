from rest_framework import serializers
from .serializers import Products,Orders,OrderItem,Cart,CartItem,Users


class CartItemSerializers(serializers.Serializer):
    cart = serializers.ForeignKey(Cart, related_name='items', on_delete=serializers.CASCADE)
    product = serializers.ForeignKey(Products, on_delete=serializers.CASCADE)
    quantity = serializers.PositiveIntegerField(default=1)
