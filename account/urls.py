from django.urls import path,include
from .views import *
from rest_framework_simplejwt.views import TokenVerifyView, TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    
    path('users/', UserListView.as_view(), name='user-list'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('UserDetailView/', UserDetailView.as_view(), name='UserDetailView'),
    
    path('groups/', GroupListCreateAPIView.as_view(), name='group-list-create'),
    path('groupss/', GroupAPIView.as_view(), name='group-list'),
    path('groupss/<int:pk>/', GroupAPIView.as_view(), name='group-retrieve-update-delete'),
          
    path('add_user_to_group/', add_user_to_group, name='add_user_to_group'),
    path('user_permissions/', UserPermissionView.as_view(), name='user_permissions'),







]