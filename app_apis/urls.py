from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'order', views.OrderViewSet)
router.register(r'orderitem', views.OrderItemViewSet)
router.register(r'product', views.ProductViewSet)
router.register(r'customer', views.CustomerViewSet)
router.register(r'product-simple', views.ProductSimpleViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]