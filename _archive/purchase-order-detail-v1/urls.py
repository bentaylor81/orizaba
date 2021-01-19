from django.urls import path
from . import views
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [   
    path('purchase-orders/<pk>', PurchaseOrderDetail.as_view(), name='purchase-order-detail'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
