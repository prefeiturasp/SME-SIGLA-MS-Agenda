from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse


def healthcheck(_request):
    return JsonResponse({"status": "ok"})

urlpatterns = [
    path('ms-agenda/api/v1/', include('agenda.urls')),
    path('ms-agenda/', healthcheck, name='healthcheck'),
    path('admin/', admin.site.urls),
] 
