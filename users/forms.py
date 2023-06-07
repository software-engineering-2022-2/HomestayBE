from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User

class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password1', 'password2')

class UserLoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ('email', 'password')
