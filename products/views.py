from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination


class CustomPagination(PageNumberPagination):
    page_size = 4  # Số lượng mục trên mỗi trang
    page_size_query_param = 'page_size'  # Tham số truy vấn để chỉ định số lượng mục trên mỗi trang
    # max_page_size = 1  # Số lượng mục tối đa trên mỗi trang
    
    
class ProductView(APIView):    
    # permission_classes = [IsAuthenticated]


    # def get(self, request,format=None):

    #     # http://127.0.0.1:8000/api/products?Category=vegetable
    #     Category = self.request.query_params.get('Category')
    #     if Category:
    #         queryset = Product.objects.filter(Category__Category_name=Category)
    #     else:
    #         queryset = Product.objects.all()
    #     # image
    #     serializer = ProductSerializer(queryset, context={"request": request}, many=True)

    #     # http://127.0.0.1:8000/api/products?Category=vegetable
        
    #     return Response({'count': len(serializer.data), 'data' :serializer.data})
    
    def get(self, request, format=None):
        Category = self.request.query_params.get('Category')
        if Category:
            queryset = Product.objects.filter(Category__Category_name=Category)
        else:
            queryset = Product.objects.all()

        # Áp dụng phân trang
        paginator = CustomPagination()
        paginated_queryset = paginator.paginate_queryset(queryset, request)

        # Serialize dữ liệu phân trang
        serializer = ProductSerializer(paginated_queryset, context={"request": request}, many=True)

        # Trả về dữ liệu phân trang
        return paginator.get_paginated_response({'count': paginator.page.paginator.count, 'data': serializer.data})
    




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