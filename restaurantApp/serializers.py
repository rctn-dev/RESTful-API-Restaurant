from rest_framework import serializers 
from django.contrib.auth.models import User 
from restaurantApp.models import MenuItem, Cart, Order, OrderItem, Category

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields='__all__'
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=Category
        fields='__all__'

class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model=MenuItem
        fields='__all__'

class CartSerializer(serializers.ModelSerializer):
    user=serializers.StringRelatedField(read_only=True)
    unit_price = serializers.DecimalField(max_digits=6, decimal_places=2, source='menuitem.price', read_only=True)
    menuitem_name=serializers.CharField(source='menuitem.title',read_only=True)
    class Meta:
        model = Cart
        fields=['user','menuitem','menuitem_name','quantity','unit_price','price']
        read_only_fields=["price"]
        
class OrderItemSerializer(serializers.ModelSerializer):

    class  Meta:
        model=OrderItem
        fields='__all__'


class OrderSerializer(serializers.ModelSerializer):
    user=serializers.StringRelatedField()
    delivery_crew=serializers.StringRelatedField()
    class  Meta:
        model=Order
        fields='__all__'
        read_only_fields=["user","total"]



    