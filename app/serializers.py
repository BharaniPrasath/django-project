from rest_framework.serializers import ModelSerializer
from django.contrib.auth import get_user_model
from .models import Cart, CartItem, MobileProduct
from rest_framework import serializers


from . import models

class serProduct(ModelSerializer):
    class Meta:
        model=models.MobileProduct
        fields='__all__'
        


# shop/serializers.py


class MobileProductSerializer(ModelSerializer):
    class Meta:
        model = MobileProduct
        fields = ["id", "productName", "productPrice", "discountPrice","productImage1","brandName"]



# cart
class CartItemSerializer(ModelSerializer):
    product = MobileProductSerializer(read_only=True)

    class Meta:
        model = CartItem
        fields = ["id", "product", "quantity", "total"]


class CartSerializer(ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = ["id", "items", "total_price"]