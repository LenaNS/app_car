from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegistrationForm(UserCreationForm):
    """
    Форма для регистрации пользователя.
    """

    class Meta:
        """
        В форму включены поля логина, пароля и повторного ввода пароля.
        """

        model = User
        fields = ["username", "password1", "password2"]
