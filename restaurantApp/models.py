from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Category(models.Model):
    slug=models.SlugField()
    title=models.CharField(max_length=255, db_index=True)
    def __str__(self):
        return self.title
    class Meta:
        verbose_name_plural = "Categories"
    
class MenuItem(models.Model): 
    category=models.ForeignKey(Category,on_delete=models.PROTECT)
    title=models.CharField(max_length=255, db_index=True)
    price=models.DecimalField(max_digits=6, decimal_places=2, db_index=True)
    featured=models.BooleanField(db_index=True)
    def __str__(self):
        return self.title
    class Meta:
        verbose_name_plural = "Menu Items"

class Cart(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    menuitem=models.ForeignKey(MenuItem, on_delete=models.CASCADE)  
    quantity=models.SmallIntegerField()
    # If you do not put a default value for unit_price and price, big problem, integrity error!!!
    unit_price=models.DecimalField(max_digits=6, decimal_places=2, default=0)
    price=models.DecimalField(max_digits=6, decimal_places=2,default=0)

    class Meta:
        unique_together=['user','menuitem']
    
    def __str__(self):
        return f'({self.user}, {self.menuitem})'

class Order(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    delivery_crew=models.ForeignKey(User, on_delete=models.CASCADE, related_name="delivery_crew", null=True)
    status=models.BooleanField(default=0, db_index=True)
    total=models.DecimalField(max_digits=6, decimal_places=2)
    date=models.DateTimeField(auto_now=True, db_index=True)
    
    def __str__(self):
        return f'({self.user}, {self.date})'

class OrderItem(models.Model):
    order=models.ForeignKey(Order, on_delete=models.CASCADE)
    menuitem=models.ForeignKey(MenuItem,on_delete=models.CASCADE)
    quantity=models.SmallIntegerField()
    unit_price=models.DecimalField(max_digits=6, decimal_places=2)
    price=models.DecimalField(max_digits=6, decimal_places=2)
    
    class Meta:
        unique_together=['order','menuitem']
        verbose_name_plural = "Order Items"

    def __str__(self):
        return f'({self.order.user}, {self.menuitem})'
    
    
