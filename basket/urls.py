from django.urls import path

from basket import views as basket

app_name = 'basket'

urlpatterns = [
    path('', basket.basket, name='basket'),
    path('add/<int:pk>/', basket.add, name='add'),
    path('remove/<int:pk>/', basket.remove, name='remove'),
]
