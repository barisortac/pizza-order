from django.urls import path, include

app_name = 'api'


urlpatterns = [
    # path('pizza/', include(('pizza.urls', 'pizza'), namespace='pizza')),
    path('order/', include(('order.urls'))),
    path('customer/', include(('customer.urls'))),
]
