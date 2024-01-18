from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from .serializers import *
from rest_framework import generics
from django.contrib.auth import authenticate


class RegisterView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        first_name= request.data.get('first_name')
        last_name= request.data.get('last_name')
        email= request.data.get('email')
        # phone=request.data.get('phone')
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # is_staff = request.data.get('is_staff', False)

        user = User(username=username,first_name=first_name,last_name=last_name,email=email)
        user.set_password(password)
        # user.is_staff = is_staff  # Cập nhật trạng thái STAFF
        user.save()

        refresh = RefreshToken.for_user(user)
        token = refresh.access_token
        
        # return redirect('home')  # Điều hướng đến trang chủ sau khi đăng ký thành công
        # else:
        #     form = UserRegistrationForm()
        #     return render(request, 'registration/register.html', {'form': form})

        return Response({
                'status': 'success',
                'user_id': user.id,
                'username': user.username,
                'is_staff': user.is_staff,
                'email':user.email,
                'first_name':user.first_name,
                'last_name':user.last_name,
                'refresh': str(refresh),
                'access': str(refresh.access_token)
        })
        

class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    


class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        # Xác thực người dùng
        user = authenticate(username=username, password=password)

        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                'status': 'success',
                'user_id': user.id,
                'username': user.username,
                'is_staff': user.is_staff,
                'email':user.email,
                'first_name':user.first_name,
                'last_name':user.last_name,
                'refresh': str(refresh),
                'access': str(refresh.access_token)

            })
        else:
            return Response({
                'status': 'error',
                'message': 'Invalid username or password'
            }, status=status.HTTP_401_UNAUTHORIZED)
            

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get('refresh_token')

        if refresh_token:
            try:
                token = RefreshToken(refresh_token)
                token.blacklist()
                return Response({'status': 'success', 'message': 'Logged out successfully.'})
            except Exception as e:
                return Response({'status': 'error', 'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'status': 'error', 'message': 'Refresh token is required.'}, status=status.HTTP_400_BAD_REQUEST)