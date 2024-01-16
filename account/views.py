from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User


class RegisterView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        # is_staff = request.data.get('is_staff', False)

        user = User(username=username)
        user.set_password(password)
        # user.is_staff = is_staff  # Cập nhật trạng thái STAFF
        user.save()

        refresh = RefreshToken.for_user(user)
        token = refresh.access_token

        return Response({
            "status": "success",
            "user_id": user.id,
            "is_staff": user.is_staff,  # Lấy giá trị mới của is_staff
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        })