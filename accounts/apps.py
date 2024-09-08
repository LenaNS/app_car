from django.apps import AppConfig


class AccountsConfig(AppConfig):
    """
    Конфигурация приложения управления пользователями.

    Поля
    ----
    default_auto_field:
        Тип по-умолчанию для автоинкрементых полей.
    name:
        Путь к модулю приложения.
    verbose_name:
        Имя приложения.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "accounts"
    verbose_name = "Пользователи"
