from rest_framework.routers import DefaultRouter

from . import views


router = DefaultRouter()
router.register('', views.CustomerViewSet, basename='customer')

urlpatterns = router.urls