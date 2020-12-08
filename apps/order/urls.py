from rest_framework.routers import DefaultRouter

from . import views


router = DefaultRouter()
router.register('', views.OrderViewSet, basename="order")
router.register('item', views.OrderItemViewSet, basename="item")

urlpatterns = router.urls