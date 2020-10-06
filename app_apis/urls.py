from django.urls import include, path
from rest_framework import routers
from app_apis import views

router = routers.DefaultRouter()
router.register(r'order', views.OrderViewSet)
router.register(r'orderitem', views.OrderItemViewSet)
router.register(r'product-simple', views.ProductSimpleViewSet)
router.register(r'product', views.ProductViewSet)
router.register(r'customer', views.CustomerViewSet)


urlpatterns = [
    path('', include((router.urls, 'app_apis'))),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]