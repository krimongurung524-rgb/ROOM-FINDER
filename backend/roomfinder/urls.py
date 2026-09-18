from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('properties.urls')),
    # path('accounts/', include('accounts.urls')),      # add once ready
    # path('dashboard/', include('dashboard.urls')),    # add once ready
    # path('chat/', include('chat.urls')),              # add once ready
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
