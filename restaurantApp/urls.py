
from django.urls import path,include
from restaurantApp import views
from rest_framework.routers import DefaultRouter

router=DefaultRouter()
router.register(r'menu-items', views.MenuItemViewSet)
router.register(r'categories', views.CategoryViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('', include('djoser.urls.authtoken')),
    path('groups/manager/users/',views.managers),
    path('groups/manager/users/<int:pk>',views.managers_detail),
    path('groups/delivery-crew/users/',views.delivery_crew),
    path('groups/delivery-crew/users/<int:pk>',views.delivery_crew_detail),
    path('cart/menu-items/', views.CartListCreateView.as_view()),
    path('orders/', views.OrderListCreateView.as_view()),
    path('orders/<int:pk>', views.OrderRUDAPIView.as_view()),

]
