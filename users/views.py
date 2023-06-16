from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.urls import reverse
from django.views import View
from .forms import UserRegistrationForm, UserLoginForm
from django.shortcuts import redirect
from django.contrib.auth import logout


class UserSignupView(CreateView):
    form_class = UserRegistrationForm
    template_name = 'users/signup.html'
    success_url = reverse_lazy('users:login')


class UserLoginView(LoginView):
    form_class = UserLoginForm
    template_name = 'users/login.html'

    def get_success_url(self):
        return reverse_lazy('home')


class UserLogoutView(View):
    def get(self, request):
        logout(request)
        return redirect(reverse('home'))
