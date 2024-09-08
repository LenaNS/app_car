from typing import Any
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import redirect_to_login
from django.core.exceptions import PermissionDenied
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import resolve_url
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.views.generic.edit import ModelFormMixin


from .models import *
from .forms import *

__all__ = [
    "CarListView",
    "CarCreateView",
    "CarDetailView",
    "CarUpdateView",
    "CarDeleteView",
]


class CarBaseView:
    """
    Базовое представление объектов модели Car.

    Поля
    ----
    model:
        Объект модели Car.
    context_object_name:
        Контекстное имя объекта модели.
    """

    model = Car
    context_object_name = "car"


class CarListView(CarBaseView, ListView):
    """
    Представление отображения списка автомобилей.

    Поля
    ----
    template_name:
        Используемый HTML шаблон.
    context_object_name:
        Контекстное имя объектов модели.
    """

    template_name = "cars/cars_list.html"
    context_object_name = "cars"


class CarCreateView(CarBaseView, LoginRequiredMixin, CreateView):
    """
    Представление для добавления автомобилей.
    Добавлять автомобили могут только зарегистрированные пользователи.

    Поля
    ----
    form_class:
        Класс формы добавления автомобилей.
    template_name:
        Используемый HTML шаблон.
    """

    form_class = CarForm
    template_name = "cars/car_create.html"

    def form_valid(self, form: CarForm) -> HttpResponseRedirect:
        """
        Обработка валидной формы автомобилей.
        Перед сохранением текущий пользователь устанавливается в качестве владельца автомобиля.

        Параметры
        ----------
        form:
            Валидная форма с данными об автомобиле.

        Возвращает
        -------
        HttpResponseRedirect:
            После успешного добавления автомобиля выполняется перенаправление на страницу автомобиля.
        """
        car = form.save(commit=False)
        car.owner = self.request.user
        car.save()
        return super().form_valid(form)

    def get_success_url(self) -> str:
        """
        Возвращает:
            После успешного добавления автомобиля формируется URL на страницу этого автомобиля.
        """
        return reverse("cars:car_detail", kwargs={"pk": self.object.pk})


class CarDetailView(CarBaseView, ModelFormMixin, DetailView):
    """
    Представление для просмотра конкретных автомобилей.

    Поля
    ----
    form_class:
        Класс формы добавления комментариев.
    template_name:
        Используемый HTML шаблон.
    """

    form_class = CommentForm
    template_name = "cars/car_detail.html"

    def form_valid(self, form: CommentForm) -> HttpResponseRedirect:
        """
        Обработка валидной формы комментариев.
        Перед сохранением комментарий привязывается к текущему автомобилю,
        текущий пользователь устанавливается в качестве автора комментария.

        Параметры
        ----------
        form:
            Валидная форма с данными комментария.

        Возвращает
        -------
        HttpResponseRedirect:
            После успешного добавления комментария выполняется перенаправление на страницу этого автомобиля.
        """
        comment = form.save(commit=False)
        comment.car = self.get_object()
        comment.author = self.request.user
        comment.save()
        return super().form_valid(form)

    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        """
        Обработка POST-запроса добавления комментария.
        Комментарии могут оставлять только зарегистрированные пользователи.

        Параметры
        ----------
        request:
            Объект запроса.
        args:
            Дополнительные неименованные аргументы.
        kwargs:
            Дополнительные именованные аргументы.

        Возвращает
        -------
        HttpResponse:
            После успешного добавления комментария выполняется перенаправление на страницу этого автомобиля.
            Если пользователь не авторизован выполняется перенаправление на страницу авторизации.
        """
        form = self.get_form()
        self.object = self.get_object()
        if request.user.is_authenticated:
            if form.is_valid():
                return self.form_valid(form)

            return self.form_invalid(form)

        return self.render_to_response(
            self.get_context_data(
                form=form,
                error_message="Оставлять комментарии могут только зарегистрированные пользователи.",
            )
        )

    def get_success_url(self) -> str:
        """
        Возвращает
        -------
            После успешного добавления комментария формируется URL на страницу этого автомобиля.
        """
        return reverse("cars:car_detail", kwargs={"pk": self.get_object().pk})


class CarEditView(CarBaseView, LoginRequiredMixin, UserPassesTestMixin):
    """
    Базовое представление обновления и удаления автомобилей.
    Операции обновления и удаления доступны только владельцу автомобиля.

    Поля
    ----
    permission_denied_message:
        Сообщение о нехватке прав доступа.
    """

    permission_denied_message = "Учетная запись не имеет прав доступа к этой операции."

    def test_func(self) -> bool:
        """
        Проверка прав доступа к объекту.

        Возвращает
        -------
        bool:
            True если пользователь является владельцем автомобиля.
        """
        return self.request.user == self.get_object().owner

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        """
        Обработка запросов.

        Параметры
        ----------
        request:
            Объект запроса.
        args:
            Дополнительные неименованные аргументы.
        kwargs:
            Дополнительные именованные аргументы.

        Возвращает
        -------
        HttpResponse:
            Предоставляет страницу редактирования автомобиля.
            Если пользователь не авторизован или не является владельцем автомобиля выполняется
            перенаправление на страницу авторизации.
        """
        try:
            return super().dispatch(request, *args, **kwargs)
        except PermissionDenied as exc:
            return self.handle_permission_denied()

    def handle_permission_denied(self) -> HttpResponseRedirect:
        """
        Обработка случая нехватки прав доступа.

        Возвращает
        -------
        HttpResponseRedirect:
            Выполняется перенаправление на страницу авторизации.
        """
        path = self.request.get_full_path()
        resolved_login_url = resolve_url(self.get_login_url())
        return redirect_to_login(
            path,
            resolved_login_url,
            self.get_redirect_field_name(),
        )


class CarUpdateView(CarEditView, UpdateView):
    """
    Представление для удаления автомобилей.

    form_class:
        Класс формы добавления комментариев.
    template_name:
        Используемый HTML шаблон.
    """

    form_class = CarForm
    template_name = "cars/car_update.html"

    def get_success_url(self) -> str:
        """
        Возвращает
        -------
            После успешного добавления комментария формируется URL на страницу этого автомобиля.
        """
        return reverse("cars:car_detail", kwargs={"pk": self.object.pk})


class CarDeleteView(CarEditView, DeleteView):
    """
    Представление для удаления автомобилей.

    Поля
    ----
    success_url:
        При успешного удаления автомобиля выполняется перенаправление на страницу автомобилей.
    """

    success_url = reverse_lazy("cars:cars_list")
