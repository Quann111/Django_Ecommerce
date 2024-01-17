from django.shortcuts import render
from datetime import datetime
# Create your views here.
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import *
from rest_framework.permissions import IsAuthenticated
from .serializers import*


class CartView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        cart = Cart.objects.filter(user=user, ordered=False).first()
        queryset = CartItem.objects.filter(cart=cart)
        serializer = CartItemSerializer(queryset, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        data = request.data
        user = request.user
        cart, _ = Cart.objects.get_or_create(user=user, ordered=False)
        cart=Cart.objects.filter(user=user)
        product = Product.objects.get(id=data.get('product'))
        price = product.Price
        quantity = data.get('quantity')
        cart_item = CartItem(user=user, product=product, quantity=quantity, cart=cart, price=price, time=datetime.now())
        cart_item.save()

        # # Tính tổng giá trị giỏ hàng
        # total_price = 0
        # cart_items = CartItem.objects.filter(user=user, cart=cart,price=price)
        # for item in cart_items:
        #     total_price += item.price

        # cart.total_price = total_price 
        # cart.save()
        # return Response({'success': 'Done', 'total_price': cart.total_price})

    def update(self,request):
        pass
    def delete(self,request):
        pass
    
