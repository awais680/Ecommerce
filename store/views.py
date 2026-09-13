from django.shortcuts import render
from django.db import transaction
from rest_framework import viewsets,status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from .models import category,product,cart,cart_item,order_item,order
from .serializers import categoryserializer,productserializer,cart_itemserializer,cartserializer,orderserializer,order_itemserializer
class categoryviewset(viewsets.ModelViewSet):
    queryset=category.objects.all()
    serializer_class=categoryserializer
class productviewset(viewsets.ModelViewSet):
    queryset=product.objects.all()
    serializer_class=productserializer
class cartviewset(viewsets.ModelViewSet):
    queryset=cart.objects.all()
    serializer_class=cartserializer
    permission_classes=[IsAuthenticated]
    def get_queryset(self):
        return cart.objects.filter(user=self.request.user)
    @action(detail=False,methods=['POST'],url_path='add-to-cart')
    def add_to_cart(self,request):
        user=request.user
        product_id=request.data.get('product_id')
        quantity=int(request.data.get('quantity',1))
        cart, _=cart.objects.get_or_create(user=user)
        try:
            product=product.objects.get(id=product_id)
        except product.doesNotExist:
            return Response({'error':'product not found'},status=status.HTTP_404_NOT_FOUND)
        if product.stock<quantity:
            return Response({'error':'not enough stock'},status=status.HTTP_404_NOT_FOUND)
        cart,created = cart_item.objects.get_or_create(cart=cart,product=product) 
        if not created :
            cart.quantity += quantity
        else:
            cart.quantity = quantity
        cart.save()
        return Response({'message':'add to cart successfully'},status=status.HTTP_200_OK)
            
class orderviewset(viewsets.ModelViewSet):
    serializer_class=orderserializer
    permission_classes=[IsAuthenticated]
    def get_queryset(self):
        return order.objects.filter(user=self.request.user)
    @action (detail=False,methods=['POST'],url_path='checkout')
    @transaction.atomic
    def checkout(self,request):
        user=request.user  
        cart=cart.objects.filter(user=user).first()
        if not cart or not cart.items.exist():
            return Response({'error':'no items in cart'},status=status.HTTP_400_BAD_REQUEST)
        total_price=0
        for item in cart.items.all():
            total_price += item.product.price * item.quantity
        order=order.objects.create(
            user=user,
            total_price=total_price,
            status='pending')
        for item in cart.items.all():
            order_item.objects.create(
                order=order,
                product=item.product,
                price=item.product.price,
                quantity=item.quantity
            )
            item.product.stock -= item.quantity
            item.product.save()
        cart.items.all().delete()
        return Response({
            'message':'order successfuly places',
            'order_id':order.id,
            'total_price':total_price
        },status=201)
# Create your views here.
