from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

admin.site.site_header = "Shop Admin Panel"
admin.site.site_title = "Shop Admin"
admin.site.index_title = "Manage Your Shop Website"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('shop.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
