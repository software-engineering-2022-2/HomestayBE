from django.urls import path

from . import views

app_name = "users"
urlpatterns = [
    path("signup/", views.UserSignupView.as_view(), name="signup"),
    path("login/", views.UserLoginView.as_view(), name="login"),
    path("logout/", views.UserLogoutView.as_view(), name="logout"),
]
