from django import forms
from .models import *

__all__ = ["CarForm", "CommentForm"]


class CarForm(forms.ModelForm):
    """
    Форма для создания или редактирования автомобилей.
    """

    class Meta:
        """
        В форму включены все поля, кроме даты создания, обновления и владельца.
        """

        model = Car
        exclude = ["created_at", "updated_at", "owner"]


class CommentForm(forms.ModelForm):
    """
    Форма для создания комментариев.
    """

    class Meta:
        """
        В форму включено только содержимое.
        """

        model = Comment
        fields = ["content"]
