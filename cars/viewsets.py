from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from django.db.models.query import QuerySet

from .serializers import *
from .permissions import *
from .models import *

__all__ = [
    "CarViewSet",
    "CommentViewSet",
]


class CarViewSet(ModelViewSet):
    """
    Представление для обработки CREATE, PUT, PATCH, GET (ALL), DELETE операций управления автомобилями.

    Поля
    ----
    queryset: QuerySet[Car]
        Стандартный набор объектов Car.
    serializer_class:
        Стандартный используемый сериализатор.
    permission_classes:
        Политики предоставления доступа.
    """

    queryset = Car.objects
    serializer_class = CarSerializer
    permission_classes = [IsCarOwnerOrReadOnly]

    def perform_create(self, serializer: CarSerializer) -> None:
        """
        Создание экземпляра объекта Car.

        Параметры
        ----------
        serializer:
            Сериализатор с валидными данными.
        """
        serializer.save(owner=self.request.user)


class CommentViewSet(CreateModelMixin, ListModelMixin, GenericViewSet):
    """
    Представление для обработки CREATE, GET ALL операций управления комментариями.

    Поля
    ----
    serializer_class:
        Стандартный используемый сериализатор.
    permission_classes:
        Политики предоставления доступа.
    """

    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self) -> QuerySet[Comment]:
        """
        Получение набора объектов Comment текущего Car.
        Если обращения происходит от несуществующего Car, возвращается ошибка.

        Возвращает
        -------
        QuerySet[Comment]:
            Набор объектов Comment текущего Car, если Car существует.
        
        Исключения
        -----------
        NotFound:
            Отсутствие данных критично для обработки запроса.
        """
        car_pk = self.kwargs["car_pk"]
        if not Car.objects.filter(pk=car_pk).exists():
            raise NotFound(detail="No Car matches the given query.")
        return Comment.objects.filter(car=car_pk)

    def perform_create(self, serializer: CommentSerializer) -> None:
        """
        Создание экземпляра объекта Comment.

        Параметры
        ----------
        serializer:
            Сериализатор с валидными данными.
        """
        car = Car.objects.get(pk=self.kwargs["car_pk"])
        serializer.save(car=car, author=self.request.user)
