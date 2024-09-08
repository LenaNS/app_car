from rest_framework.serializers import ModelSerializer

from .models import *

__all__ = ["CarSerializer", "CommentSerializer"]


class CarSerializer(ModelSerializer):
    """
    Сериализатор для GET (ALL), CREATE, PUT/PATCH, DELETE операций с объектами Car.
    """

    class Meta:
        """
        В сериализатор включены все поля.
        Владелец автомобиля доступен только для чтения.
        """

        model = Car
        fields = "__all__"
        read_only_fields = ["owner"]


class CommentSerializer(ModelSerializer):
    """
    Сериализатор для GET ALL, CREATE операций с объектами Comment.
    """

    class Meta:
        """
        В сериализатор включены все поля, кроме car,
        т.к. комментарии можно получить только у конкретной машины.
        Автор комментария доступен только для чтения.
        """

        model = Comment
        exclude = ["car"]
        read_only_fields = ["author"]
