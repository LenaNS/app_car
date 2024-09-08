from django.db import models
from django.contrib.auth.models import User


__all__ = ["Car", "Comment"]


class Car(models.Model):
    """
    Модель автомобилей.

    Поля
    ----
    make:
        Марка автомобиля.
    model:
        Модель автомобиля.
    year:
        Год выпуска.
    description:
        Описание автомобиля.
    created_at:
        Дата создания записи об автомобиле.
    updated_at:
        Дата обновления записи об автомобиле.
    owner:
        Владелец автомобиля.
    """

    make = models.CharField(max_length=100, verbose_name="Марка")
    model = models.CharField(max_length=100, verbose_name="Модель")
    year = models.IntegerField(verbose_name="Год выпуска")
    description = models.TextField(verbose_name="Описание")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создан")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Обновлен")
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="cars", verbose_name="Владелец"
    )

    def __str__(self) -> str:
        """
        Возвращает
        -------
        str:
            Строковое представление модели.
        """
        return "%s %s (%s)" % (self.make, self.model, self.year)

    class Meta:
        verbose_name = "Автомобиль"
        verbose_name_plural = "Автомобили"


class Comment(models.Model):
    """
    Модель комментариев пользователей.

    Поля
    ----
    content:
        Текст комментария.
    created_at:
        Дата создания комментария.
    car:
        Автомобильный к которому оставлен комментарий.
    author:
        Автор комментария.
    """

    content = models.TextField(verbose_name="Комментарий")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создан")
    car = models.ForeignKey(
        Car,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Автомобиль",
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="comments", verbose_name="Автор"
    )

    def __str__(self) -> str:
        """
        Возвращает
        -------
        str:
            Строковое представление модели.
        """
        return "Комментарий пользователя %s от %s" % (self.author, self.created_at)

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"
