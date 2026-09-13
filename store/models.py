from django.db import models
from django.contrib.auth.models import User
class category(models.Model):
    name=models.CharField(max_length=50)
    slug=models.SlugField(unique=True)
    def __str__(self):
        return self.name
class product(models.Model):
    category=models.ForeignKey(category, on_delete=models.CASCADE)
    name=models.CharField(max_length=100)
    description=models.TextField()
    price=models.DecimalField(max_digits=8, decimal_places=2)
    stock=models.PositiveIntegerField(default=0)
    created_at=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name
class cart(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
class cart_item(models.Model):
        cart=models.ForeignKey(cart,on_delete=models.CASCADE)
        product=models.ForeignKey(product,on_delete=models.CASCADE)
        quantity=models.IntegerField()
class order(models.Model):
    STATUS_CHOICES = [
    ('PENDING', 'Pending'),
    ('COMPLETED', 'Completed'),
    ('CANCELLED', 'Cancelled'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    total_price=models.DecimalField(max_digits=8, decimal_places=2)
    created_at=models.DateTimeField(auto_now_add=True)
class order_item(models.Model):
     order=models.ForeignKey(order,on_delete=models.CASCADE)
     product=models.ForeignKey(product,on_delete=models.CASCADE)
     quantity=models.PositiveIntegerField()
     price=models.DecimalField(max_digits=8, decimal_places=2)

     
        



# Create your models here.


print("models.py file executed successfully")