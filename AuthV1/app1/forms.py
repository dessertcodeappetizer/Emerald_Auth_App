from django.contrib.auth.forms import UserCreationForm
from .models import User_auth

class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User_auth
        fields = ['first_name', 'last_name', 'username', 'email', 'phone', 'password1', 'password2', 'gender']