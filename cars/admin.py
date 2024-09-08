from typing import Any
from django.contrib.admin import ModelAdmin, register
from django.http import HttpRequest
from .models import *


@register(Car)
class CarAdmin(ModelAdmin):
    """
    Панель администрирования автомобилей.
    Разрешен только просмотр и удаление.

    Поля
    ----
    list_display:
        Список отображаемых полей.
    list_filter:
        Список полей, по которым доступны фильтры.
    search_fields:
        Список полей по которым выполняется поиск.
    """

    list_display = (
        "owner",
        "make",
        "model",
        "year",
        "description",
        "updated_at",
        "created_at",
    )
    list_filter = ("owner", "make", "model", "year", "updated_at", "created_at")
    search_fields = ("description",)

    def has_add_permission(self, request: HttpRequest) -> bool:
        """
        Определение прав на добавление автомобилей.

        Параметры
        ----------
        request:
            Объект запроса.

        Возвращает
        -------
        bool:
            Добавление автомобилей через админку запрещено.
        """
        return False

    def has_change_permission(self, request: HttpRequest, obj: Car = None) -> bool:
        """
        Определение прав на редактирование автомобилей.

        Параметры
        ----------
        request:
            Объект запроса.
        obj:
            Объект модели.

        Возвращает
        -------
        bool:
            Редактирование автомобилей через админку запрещено.
        """
        return False


@register(Comment)
class CommentAdmin(ModelAdmin):
    """
    Панель администрирования комментариев.
    Разрешен только просмотр и удаление.

    Поля
    ----
    list_display:
        Список отображаемых полей.
    list_filter:
        Список полей, по которым доступны фильтры.
    search_fields:
        Список полей по которым выполняется поиск.
    """

    list_display = ("author", "content", "car", "created_at")
    list_filter = ("car", "author", "created_at")
    search_fields = ("content",)

    def has_add_permission(self, request: HttpRequest) -> bool:
        """
        Определение прав на добавление комментариев.

        Параметры
        ----------
        request:
            Объект запроса.

        Возвращает
        -------
        bool:
            Добавление комментариев через админку запрещено.
        """
        return False

    def has_change_permission(self, request: HttpRequest, obj: Comment = None) -> bool:
        """
        Определение прав на редактирование комментариев.

        Параметры
        ----------
        request:
            Объект запроса.
        obj:
            Объект модели.

        Возвращает
        -------
        bool:
            Редактирование комментариев через админку запрещено.
        """
        return False
