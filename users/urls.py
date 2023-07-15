from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('', views.endpoints),
    path('users/', views.UserList.as_view(), name='users'),
    path('users/<str:username>/avatar/', views.UserUpdateAvatar.as_view(), name='user_avatar'),
    path('users/<str:username>/password/', views.UserUpdatePassword.as_view(), name='user_password'),
    path('users/<str:username>/', views.UserDetail.as_view(), name='user_detail'),
    path('users/manager_profile/<str:id>/', views.ManagerProfile.as_view(), name='manager_profile'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
