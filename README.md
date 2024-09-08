# Веб-приложение для управления информацией об автомобилях с использованием API
## Используемый стек
```
Python 3.12
Django 5.0
Django Rest Framework 3.15
SQLite 3
```
## Функции
```
Управление автомобилями:
- все пользователи могут просматривать доступный список автомобилей;
- все пользователи могут просматривать подробную информацию о каждом автомобиле;
- только зарегистрированные пользователи могут добавлять новые автомобили в систему;
- пользователи могут редактировать и удалять только свои собственные записи об автомобилях.

Управление комментариями:
- зарегистрированные пользователи могут оставлять комментарии к автомобилям;
- комментарии отображаются под соответствующими автомобилями.

Регистрация и авторизация:
- реализована возможность регистрации новых пользователей.
- пользователи могут входить в систему и управлять только своими автомобилями.

Административная панель:
- модели автомобилей и комментариев доступны в административной панели Django для удобного управления и модерации;
- административная панель доступна по адресу /admin/.
```
## Установка
### 1. Клонирование репозитория
```
Клонируйте проект при помощи Git
```
##### Пример
```
git clone https://github.com/LenaNS/app_car.git
```
### 2. Установка зависимостей
```
Зависимости находятся в файле requirements.txt, воспользуйтесь pip для установки
```
##### Пример
```
pip install -r requirements.txt
```
### 3. Миграция БД (необязательно)
```
Приложение поставляется с тестовыми данными в файле db.sqlite3
Если Вы хотите использовать чистую БД - удалите файл db.sqlite3 и выполните миграции при помощи 'migrate'
```
##### Пример:
```
py manage.py migrate
```
## Запуск
```
Для запуска приложения выполните команду 'runserver', при необходимости укажите нужный порт
```
##### Пример:
```
py manage.py runserver localhost:8000
```
## API
### Краткое описание
```
API приложения предоставляет доступ к следующим опреациям:
- получение списка автомобилей;
- получение информации о конкретном автомобиле;
- создание нового автомобиля;
- обновление информации об автомобиле;
- удаление автомобиля;
- получение комментариев к автомобилю;
- добавление нового комментария к автомобилю.

GET запросы доступны для неавторизованных пользователей.
Создание автомобилей и комментариев доступны только для авторизованных пользователей.
Редактирование и удаление автомобилей доступны только для владельцев этих автомобилей.

Авторизация доступна по адресу /accounts/login/
```
### Подробности
#### Получить список записей об автомобилях
```
GET /api/cars/
```
##### Пример:
```
curl -X GET http://127.0.0.1:8000/api/cars/
```
#### Создать новую запись об автомобиле
```
POST /api/cars/
{
    "make": str,
    "model": str,
    "year": int,
    "description": str
}
```
##### Пример:
```
echo '{"make":"BMW", "model":"X3","year":2020,"description":"Немецкое качество"}' | curl --json @- localhost:8000/api/cars/
```
#### Получить запись об автомобиле
```
GET /api/cars/{id}/
```
##### Пример:
```
curl -X GET http://127.0.0.1:8000/api/cars/1/
```
#### Обновить запись об автомобиле
```
PUT/PATCH /api/cars/{id}/
{
    "id": int,
    "make": str,
    "model": str,
    "year": int,
    "description": str
}
```
##### Пример:
```
echo '{"id":1,"make":"BMW", "model":"X3","year":2020,"description":"Немецкое качество"}' | curl --json @- localhost:8000/api/cars/
```
#### Удалить запись об автомобиле
```
DELETE /api/cars/{id}/
```
##### Пример:
```
curl -X DELETE http://127.0.0.1:8000/api/cars/1/
```
#### Получить комментарии об автомобиле
```
GET /api/cars/{id}/comments/
```
##### Пример:
```
curl -X GET http://127.0.0.1:8000/api/cars/1/comments/
```
#### Добавить комментарий об автомобиле
```
POST /api/cars/{id}/comments/
{
    "content": str
}
```
##### Пример:
```
echo '{"content":"Надежная"}' | curl --json @- localhost:8000/api/cars/1/comments/
```