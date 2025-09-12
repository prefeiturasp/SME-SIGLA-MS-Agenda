from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse


def healthcheck(_request):
    return JsonResponse({"status": "ok"})

urlpatterns = [
    path('', healthcheck, name='healthcheck'),
    path('api/v1/', include('agenda.urls')),
    path('admin/', admin.site.urls),
] 
