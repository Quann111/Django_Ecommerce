from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import *
from rest_framework.permissions import IsAuthenticated


class ProductView(APIView):
    # permission_classes = [IsAuthenticated]

    # def get(self, request):
    #     Category = self.request.query_params.get('Category')
    #     if Category :
    #         queryset = Product.objects.filter(Category__Category_name = Category)
    #     else :
    #         queryset = Product.objects.all()
    #     serializer = ProductSerializer(queryset, many=True)
    #     return Response(serializer.data)
    
    permission_classes = [IsAuthenticated]

    def get(self, request):

        # http://127.0.0.1:8000/api/products?Category=vegetable
        Category = self.request.query_params.get('Category')
        if Category:
            queryset = Product.objects.filter(Category__Category_name=Category)
        else:
            queryset = Product.objects.all()
        serializer = ProductSerializer(queryset, many=True)
        
        # http://127.0.0.1:8000/api/products?Category=vegetable
        return Response({'count': len(serializer.data), 'data' :serializer.data})
    
    

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()   
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class DemoView(APIView):
    
    
    # egggg
    permission_classes = [IsAuthenticated]
    # egggg
    
    
    def get (self,request):
        
        return Response({'success':"gg Authenticate"})