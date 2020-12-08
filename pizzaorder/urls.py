from rest_framework.authtoken import views
from .views import MainView
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path


# TODO: ADD SWAGGER
# from drf_yasg import openapi
# from drf_yasg.views import get_schema_view
# schema_view = get_schema_view(
#    openapi.Info(
#       title="PizzaOrder API",
#       default_version='v1',
#       description="",
#       terms_of_service="",
#       contact=openapi.Contact(email="contact@pizzaorder.com"),
#       license=openapi.License(name="PizzaOrder"),
#    ),
#    public=True,
#    url="http://www.pizzaorder.com",
#    permission_classes=(permissions.AllowAny,),
# )


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('api-token-auth/', views.obtain_auth_token),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    # TODO: ADD SWAGGER
    # re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    # path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    # path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    # the 'api-root' from django rest-frameworks default router
    # http://www.django-rest-framework.org/api-guide/routers/#defaultrouter
    # re_path(r'^$', RedirectView.as_view(url=reverse_lazy('api-root'), permanent=False)),
    path('', MainView.as_view(), name="main-page"),
    # path('', include('django.contrib.auth.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



