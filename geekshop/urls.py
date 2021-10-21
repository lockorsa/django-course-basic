from django.urls import path

from geekshop import views

urlpatterns = [
    path('', views.index, name='index'),
    path('products/', views.products, name='products'),
    path('contacts/', views.contact, name='contacts'),
]
