"""Rotas de URL do módulo agenda."""

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from agenda.api.views import AgendaViewSet

router = DefaultRouter()
router.register(r"agendas", AgendaViewSet, basename="agendas")

urlpatterns = [
    path("", include(router.urls)),
]
