"""
URL configuration for the processes module.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AgendaViewSet

router = DefaultRouter()
router.register(r'agendas', AgendaViewSet, basename='agendas')

urlpatterns = [
    path('', include(router.urls)),
] 