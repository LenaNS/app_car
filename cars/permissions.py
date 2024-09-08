from rest_framework.permissions import SAFE_METHODS, IsAuthenticatedOrReadOnly
from rest_framework.request import Request
from rest_framework.views import View

from .models import *

__all__ = ["IsCarOwnerOrReadOnly"]


class IsCarOwnerOrReadOnly(IsAuthenticatedOrReadOnly):
    """
    Класс предоставления доступа на чтение, либо полного доступа владельцу автомобиля
    """

    def has_object_permission(self, request: Request, view: View, obj: Car) -> bool:
        """
        Проверка доступа к объекту

        Параметры
        ----------
        request:
            Объект запроса
        view:
            Представление, которое обрабатывает запрос
        obj:
            Экземпляр Car, доступ к которому проверяется

        Возвращает
        -------
            True, если user является владельцем объекта
        """
        return bool(request.method in SAFE_METHODS or request.user == obj.owner)
