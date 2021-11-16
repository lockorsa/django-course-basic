from django.urls import path

from geekshop import views as geekshop

app_name = 'geekshop'

urlpatterns = [
    path('products/', geekshop.products, name='products'),
    path('products/<slug:slug>/', geekshop.product_category, name='category'),
    path('product/<slug:slug>/', geekshop.product, name='product'),
]
