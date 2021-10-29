from django.urls import path

from geekshop import views as geekshop

app_name = 'geekshop'

urlpatterns = [
    path('', geekshop.index, name='index'),
    path('contacts/', geekshop.contact, name='contacts'),
    path('products/', geekshop.products, name='products'),
    path('products/<slug:slug>', geekshop.product_category, name='category'),
]
