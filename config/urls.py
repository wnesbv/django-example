
from django.views.static import serve
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static, settings


urlpatterns = (
    [

    path("ordinary/", include("user_ordinary.urls")),
    path("privileged/", include("user_privileged.urls")),

    path("", include("core.urls")),
    path("chat/", include("chat.urls")),

    path("admin/", admin.site.urls),

    ]
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT,)
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
)

urlpatterns += [
    path("media/<path:path>", serve, {"document_root": settings.MEDIA_ROOT,}),
    path("static/<path:path>", serve, {"document_root": settings.STATIC_ROOT}),
]
