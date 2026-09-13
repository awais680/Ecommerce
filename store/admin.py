from django.contrib import admin
from . import models
admin.site.register(models.category)
admin.site.register(models.product)
admin.site.register(models.cart)
admin.site.register(models.cart_item)
admin.site.register(models.order)
admin.site.register(models.order_item)

# Register your models here.
