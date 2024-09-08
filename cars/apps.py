from django.apps import AppConfig


class CarsConfig(AppConfig):
    """
    Конфигурация приложения управления автомобилями.

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
    name = "cars"
    verbose_name = "Автомобили"
