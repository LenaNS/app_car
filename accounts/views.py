from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib.auth import login
from django.views.generic.edit import CreateView

from .forms import RegistrationForm


class RegisterView(CreateView):
    """
    Представление для регистрации пользователя.

    Поля
    ----
    form_class:
        Класс формы регистрации пользователя.
    template_name:
        Используемый HTML шаблон.
    success_url:
        При успешной регистрации пользователя выполняется перенаправление на страницу автомобилей.
    """
    form_class = RegistrationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('cars:cars_list')

    def form_valid(self, form: RegistrationForm) -> HttpResponseRedirect:
        """
        Обработка валидной формы регистрации.

        Параметры
        ----------
        form:
            Валидная форма с данными пользователя.

        Возвращает
        -------
        HttpResponseRedirect:
            После успешной регистрации выполняется авторизация и перенаправление на страницу автомобилей.
        """
        response = super().form_valid(form)
        login(self.request, self.object)
        return response

