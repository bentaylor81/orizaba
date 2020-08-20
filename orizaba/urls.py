from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api', include('app_apis.urls')),
    path('', include('app_orders.urls')),
    path('', include('app_users.urls')),
    path('', include('app_products.urls')),
    path('', include('app_stats.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)