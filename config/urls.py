from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView


def healthcheck(_request):
    return JsonResponse({"status": "ok"})


_core_urlpatterns = [
    path("api/v1/", include("agenda.api.urls")),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path("", healthcheck, name="healthcheck"),
]

_static_urlpatterns = static(
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Só as rotas da app entram sob MS_PATH. Static/media ficam na raiz
# (/django_static/, /media/) para bater com STATIC_URL e MEDIA_URL
# usados pelo admin e pelo collectstatic.
if settings.DJANGO_ENVIRONMENT != "local":
    _ms_prefix = settings.MS_PATH.strip("/")
    urlpatterns = [
        path(f"{_ms_prefix}/", include(_core_urlpatterns)),
    ] + _static_urlpatterns
else:
    urlpatterns = _core_urlpatterns + _static_urlpatterns
