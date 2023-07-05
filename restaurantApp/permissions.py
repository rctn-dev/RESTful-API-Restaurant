from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsManager(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='managers').exists()

class IsManagerOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        else: 
            return request.user.groups.filter(name='managers').exists()
class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        else: 
            return request.user.is_staff
    
class IsDeliveryCrew(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='delivery_crew').exists()
    
