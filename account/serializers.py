from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *
from django.contrib.auth.models import Group
from rest_framework.serializers import ModelSerializer



class GroupSerializer(ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'

class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = '__all__'

# # 
# class UserSerializer(serializers.ModelSerializer): 
#     member = MemberSerializer(read_only=True) 
#     snippets = serializers.HyperlinkedRelatedField(many=True, view_name='snippet-detail', read_only=True) 
#     address = serializers.CharField(write_only=True) 
#     avatar = serializers.ImageField(write_only=True, default='dsd.jpg') 
 
#     class Meta: 
#         model = User 
#         fields = ['id', 'username', 'password', 'email', 'address', 'avatar', 'member'] 
#         extra_kwargs = {'password': {'write_only': True}} 
 
#     def create(self, validated_data): 
#         address = validated_data.pop("address") 
#         phone = validated_data.pop("avatar") 
     
#         user = User.objects.create(**validated_data) 
#         user.set_password(validated_data["password"]) 
#         user.save() 
 
#         member = Member.objects.create(user=user, address=address) 
         
#         return { 
#             "id": user.id, 
#             "username": user.username, 
#             "email": user.email, 
#             "address": member.address, 
#             "avatar": member.avatar.url, 
#             "member": member.id 
#         }



class UserSerializer(serializers.ModelSerializer):
    address = serializers.CharField(max_length=255,required=False)
    phone = serializers.CharField(max_length=15,required=False)

    def create(self, validated_data):
        address = validated_data("address")
        phone = validated_data.pop("phone")
        password = validated_data.pop("password")

        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()

        # Create the Member object and associate it with the User
        member = Member.objects.create(user=user, address=address, phone=phone)

        return member  # Return the Member object instead of User

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'address', 'phone']

