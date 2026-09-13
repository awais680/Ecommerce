from rest_framework import serializers
from .models import category,product,cart,cart_item,order,order_item
class categoryserializer(serializers.ModelSerializer):
    class Meta:
        model=category
        fields=['id','name','slug']


class productserializer(serializers.ModelSerializer):
    category_name=serializers.ReadOnlyField(source='category.name')
    class Meta:
        model=product
        fields=['id','category','category_name','name','description','price','stock','created_at']
class cart_itemserializer(serializers.ModelSerializer):
    product_details=productserializer(source='product',read_only=True)
    product_id=serializers.PrimaryKeyRelatedField(
        queryset=product.objects.all(),source='product',write_only=True)
    class Meta:
             model=cart_item
             fields=['id','product_details','product_id','quantity']

class cartserializer(serializers.ModelSerializer):
    item=cart_itemserializer(many=True,read_only=True)

    class Meta:
            model=cart
            fields=['id','item','created_at','item','user']

class order_itemserializer(serializers.ModelSerializer):
      product_name=serializers.ReadOnlyField(source='product.name')
      class Meta:
              model=order_item
              fields=['id','product','product_name','quantity','price']

class orderserializer(serializers.ModelSerializer):
      items=order_itemserializer(many=True,read_only=True)

      class Meta:
              model=order
              fields=['id','user','items','status','total_price','created_at']
              read_only_fields=['user','total_price','status']









    