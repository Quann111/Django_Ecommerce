from rest_framework import serializers
from .models import *


class QuantitySerializer(serializers.ModelSerializer):
    class Meta:
        model = QuantityVariant
        fields = '__all__'


class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = ColorVariant
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

    
class ProductSerializer(serializers.ModelSerializer):
    Category = serializers.SerializerMethodField()
    Quantity_type = QuantitySerializer()
    Color_type = ColorSerializer()

    class Meta:
        model = Product
        exclude = ['id']

    def get_Category(self, obj):
        category = obj.Category
        serializer = CategorySerializer(category)
        return serializer.data
    
    
# image
    def get_photo_url(self, obj):
        request = self.context.get('request')
        photo_url = obj.fingerprint.url
        return request.build_absolute_uri(photo_url)
    
