from rest_framework.routers import DefaultRouter

from . import views


router = DefaultRouter()
router.register('', views.OrderViewSet, base_name="order")
router.register('item', views.OrderItemViewSet, base_name="item")

urlpatterns = router.urls