from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from .serializers import *
from rest_framework import generics
from django.contrib.auth import authenticate
from .models import *
from rest_framework.generics import RetrieveAPIView

from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions

from rest_framework.generics import ListCreateAPIView
from rest_framework.viewsets import ModelViewSet

from django.contrib.auth.models import Group
from .serializers import GroupSerializer

from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import Group, User

from django.contrib.auth.models import User,Permission
from guardian.shortcuts import assign_perm

from django.contrib.auth.models import User
from guardian.shortcuts import assign_perm, get_objects_for_user


from guardian.shortcuts import assign_perm, get_objects_for_user
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response





class UserPermissionView(APIView):
    def post(self, request):
        username = request.data.get('username')
        permission_codename = request.data.get('permission')

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({
                'status': 'error',
                'message': 'User not found'
            }, status=status.HTTP_404_NOT_FOUND)

        try:
            permission = Permission.objects.get(codename=permission_codename)
        except Permission.DoesNotExist:
            return Response({
                'status': 'error',
                'message': 'Permission not found'
            }, status=status.HTTP_404_NOT_FOUND)

        user.user_permissions.add(permission)
        user.save()

        return Response({
            'status': 'success',
            'message': 'Permission added to user successfully'
        })



# thêm 1 người vào nhóm
@api_view(['POST'])
def add_user_to_group(request):
    try:
        username = request.data['username']
        group_name = request.data['group_name']

        user = User.objects.get(username=username)
        group = Group.objects.get(name=group_name)

        user.groups.add(group)

        return Response({'message': 'User added to group successfully'})
    except User.DoesNotExist:
        return Response({'message': 'User does not exist'}, status=400)
    except Group.DoesNotExist:
        return Response({'message': 'Group does not exist'}, status=400)

# quản lý các nhóm quyền
class GroupListCreateAPIView(ListCreateAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

class GroupAPIView(APIView):
    def get(self, request, pk=None):
        if pk is not None:
            group = Group.objects.get(pk=pk)
            serializer = GroupSerializer(group)
        else:
            groups = Group.objects.all()
            serializer = GroupSerializer(groups, many=True)

        return Response(serializer.data)

    def post(self, request):
        serializer = GroupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def put(self, request, pk):
        group = Group.objects.get(pk=pk)
        serializer = GroupSerializer(group, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, pk):
        group = Group.objects.get(pk=pk)
        group.delete()
        return Response(status=204)

# chi tiết thông tin tài khoản 1 User
class UserDetailView(RetrieveAPIView):
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    serializer_class = UserSerializer


    def get_queryset(self):
        return User.objects.all()  

    def get_object(self):
        return self.request.user
    

# đăng ký
class RegisterView(APIView):

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        first_name= request.data.get('first_name')
        last_name= request.data.get('last_name')
        email= request.data.get('email')
        phone=request.data.get('phone')
        address = request.data.get('address')
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        

        # is_staff = request.data.get('is_staff', False)

        user = User(username=username,first_name=first_name,last_name=last_name,email=email)
        member = Member(user=user,phone=phone,address=address)
        user.set_password(password)
        # user.is_staff = is_staff  # Cập nhật trạng thái STAFF
        user.save()
        member.save()
        group_name = 'Member'  # Tên nhóm bạn muốn gán người dùng vào
        group = Group.objects.get(name=group_name)
        user.groups.add(group)

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
                'phone':   member.phone,
                'address':member.address,
                'group': group.name,
                'refresh': str(refresh),
                'access': str(refresh.access_token)
        })
        


# //////////////////////////////////////////////////////////////////////////


class UserListView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    
# class UserListView(generics.ListAPIView):
#     queryset = Member.objects.all()
#     serializer_class = MemberSerializer
    



# //////////////////////////////////////////////////////////////////////////



# LoginView
class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        # Xác thực người dùng
        user = authenticate(username=username, password=password)

        group = None  # Đặt giá trị mặc định cho biến group

        if user is not None:
            refresh = RefreshToken.for_user(user)

            if group_name := request.data.get('group'):
                group = Group.objects.get(name=group_name)


        member = Member()
        member.phone = request.data.get('phone')
        member.address = request.data.get('address')

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
                'phone':   member.phone,
                'address':member.address,
                'group': group.name if group else None,
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
        if not (refresh_token := request.data.get('refresh_token')):
            return Response({'status': 'error', 'message': 'Refresh token is required.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({'status': 'success', 'message': 'Logged out successfully.'})
        except Exception as e:
            return Response({'status': 'error', 'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)