from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from restaurantApp.permissions import IsManager, IsManagerOrReadOnly, IsAdminOrReadOnly
from django.contrib.auth.models import User, Group
from rest_framework.response import Response
from restaurantApp.serializers import UserSerializer, MenuItemSerializer, CartSerializer, OrderSerializer, OrderItemSerializer, CategorySerializer
from rest_framework.generics import get_object_or_404
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from restaurantApp.models import MenuItem, Cart, Order, OrderItem,Category
from rest_framework import generics
from decimal import Decimal
from rest_framework.filters import OrderingFilter
from django_filters import rest_framework as filters



# api/menu-items
# api/menu-items/{menuItemId}
class CategoryViewSet(ModelViewSet):
    queryset=Category.objects.all()
    serializer_class=CategorySerializer
    permission_classes=[IsAuthenticated, IsManagerOrReadOnly|IsAdminOrReadOnly]
    filter_backends=[filters.DjangoFilterBackend]
    # search_fields=["category__title",'title','price','featured']
    filterset_fields = ['slug']

# api/menu-items
# api/menu-items/{menuItemId}
class MenuItemViewSet(ModelViewSet):
    queryset=MenuItem.objects.all()
    serializer_class=MenuItemSerializer
    permission_classes=[IsAuthenticated, IsManagerOrReadOnly|IsAdminOrReadOnly]
    filter_backends=[filters.DjangoFilterBackend, OrderingFilter]
    # search_fields=["category__title",'title','price','featured']
    filterset_fields = ['title','featured','category','category__title','price']
    ordering_fields=['price','category']

# api/cart/menu-items
class CartListCreateView(generics.ListCreateAPIView, generics.DestroyAPIView):
    serializer_class=CartSerializer
    permission_classes=[IsAuthenticated]

    def get_queryset(self):
        user=self.request.user
        return Cart.objects.filter(user=user)
    
    def perform_create(self, serializer):
        user=self.request.user
        menuitem=self.request.data["menuitem"]
        quantity=self.request.data["quantity"]
        unit_price=MenuItem.objects.get(pk=menuitem).price
        price=unit_price*int(quantity)
        serializer.save(user=user, price=price)
        
    def delete(self, request):
        user = self.request.user
        Cart.objects.filter(user=user).delete()
        return Response(status=204)
 
# api/orders
class OrderListCreateView(generics.ListCreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    filter_backends=[filters.DjangoFilterBackend, OrderingFilter]
    # search_fields=["category__title",'title','price','featured']
    filterset_fields = ['status','delivery_crew']
    ordering_fields=['status','date','total']
    def perform_create(self, serializer):
        cart_items = Cart.objects.filter(user=self.request.user)
        total = self.calc_total(cart_items)
        order = serializer.save(user=self.request.user, total=total)

        for item in cart_items:
            OrderItem.objects.create(order=order,menuitem=item.menuitem, quantity=item.quantity,
                                     unit_price=item.unit_price, price=item.price)
            item.delete()

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name='managers').exists():
            return Order.objects.all()
        if user.groups.filter(name='delivery_crew').exists():
            return Order.objects.filter(delivery_crew=user)
        return Order.objects.filter(user=user)

    def calc_total(self, items):
        total = Decimal(0)
        for item in items:
            total += item.price
        return total

# api/orders/{OrderId}
class OrderRUDAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class=OrderSerializer
    permission_classes=[IsAuthenticated]
    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name='managers').exists():
            return Order.objects.all()
        if user.groups.filter(name='delivery_crew').exists():
            return Order.objects.filter(delivery_crew=user)
        return Order.objects.filter(user=user)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        user=request.user
        if user.groups.filter(name='managers').exists():
            self.perform_destroy(instance)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def perform_update(self, serializer): 
        instance=self.get_object()
        data=self.request.data
        user=self.request.user
        status=data.get("status",instance.status)
        delivery_crew_char=data.get("delivery_crew")
        # foreign key den seç. ve filtrele delivery crew de mi diye
        if delivery_crew_char:
            delivery_crew_obj=User.objects.get(username=delivery_crew_char)
        else:
             delivery_crew_obj=instance.delivery_crew

        if user.groups.filter(name='managers').exists():
             serializer.save(delivery_crew=delivery_crew_obj, status=status)
        if user.groups.filter(name='delivery_crew').exists():
            serializer.save(status=status)

    
    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

# api/groups/manager/users: list, create, delete managers
@api_view(["GET","POST"])
@permission_classes([IsAuthenticated, IsManager|IsAdminUser])
def managers(request):
    if request.method=="GET":
        users=User.objects.all()
        managers=users.filter(groups__name='managers')
        serialized_items=UserSerializer(managers,many=True)
        return Response(serialized_items.data)
    if request.method=='POST':
        username=request.data['username']
        if username:
            user=get_object_or_404(User, username=username)
            manager_group=Group.objects.get(name='managers')
            manager_group.user_set.add(user)
            return Response({'message':'user added to the manager group.'},status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
@api_view(["GET","DELETE"])
@permission_classes([IsAuthenticated, IsManager|IsAdminUser])
def managers_detail(request, pk):
    try:
        user=User.objects.get(pk=pk)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)
    is_manager=user.groups.filter(name='managers').exists()
    if is_manager:
        if request.method=="GET":
            serialized_item=UserSerializer(user)
            return Response(serialized_item.data)
        if request.method=="DELETE":
            manager_group=Group.objects.get(name='managers')
            manager_group.user_set.remove(user)
            return Response({'message':'user removed from the manager group.'},status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)

# api/groups/delivery-crew/users: list, create, delete delivery_crew
@api_view(["GET","POST"])
@permission_classes([IsAuthenticated, IsManager|IsAdminUser])
def delivery_crew(request):
    if request.method=="GET":
        users=User.objects.all()
        delivery_crew=users.filter(groups__name='delivery_crew')
        serialized_items=UserSerializer(delivery_crew,many=True)
        return Response(serialized_items.data)
    if request.method=='POST':
        username=request.data['username']
        if username:
            user=get_object_or_404(User, username=username)
            delivery_crew_group=Group.objects.get(name='delivery_crew')
            delivery_crew_group.user_set.add(user)
            return Response({'message':'user added to the delivery-crew group.'},status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
@api_view(["GET","DELETE"])
@permission_classes([IsAuthenticated, IsManager|IsAdminUser])
def delivery_crew_detail(request, pk):
    try:
        user=User.objects.get(pk=pk)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)
    is_delivery_crew=user.groups.filter(name='delivery_crew').exists()
    if is_delivery_crew:
        if request.method=="GET":
            serialized_item=UserSerializer(user)
            return Response(serialized_item.data)
        if request.method=="DELETE":
            delivery_crew_group=Group.objects.get(name='delivery_crew')
            delivery_crew_group.user_set.remove(user)
            return Response({'message':'user removed from the delivery-crew group.'},status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)

