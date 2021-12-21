from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path


from .routers import router
from .swagger_config import swagger_url_patterns

urlpatterns = swagger_url_patterns +[
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
#    path("api/images/", views.list_pictures)

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
        path("api/__debug__/", include(debug_toolbar.urls)),
    ] + urlpatterns
