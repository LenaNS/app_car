"""
Поля
----
car_patterns:
    Набор url представлений пользовательского интерфейса
router:
    Набор url представлений API
"""

from rest_framework.routers import DefaultRouter
from django.shortcuts import redirect
from django.urls import include, path
from .views import *
from .viewsets import *


car_patterns = (
    [
        path("", CarListView.as_view(), name="cars_list"),
        path("create/", CarCreateView.as_view(), name="car_create"),
        path("<int:pk>/", CarDetailView.as_view(), name="car_detail"),
        path("<int:pk>/edit/", CarUpdateView.as_view(), name="car_edit"),
        path("<int:pk>/delete/", CarDeleteView.as_view(), name="car_delete"),
    ],
    "cars",
)

router = DefaultRouter()
router.register(r"cars", CarViewSet, basename="cars")
router.register(r"cars/(?P<car_pk>[^/.]+)/comments", CommentViewSet, basename="comment")

urlpatterns = [
    path("", lambda request: redirect("cars:cars_list", permanent=True)),
    path("cars/", include(car_patterns)),
    path("api/", include(router.urls)),
]
