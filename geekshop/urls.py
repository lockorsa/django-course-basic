from django.urls import path

from geekshop import views as geekshop

app_name = 'geekshop'

urlpatterns = [
    path('products/', geekshop.root, name='products'),
    path('products/<slug:slug>/', geekshop.products, name='category'),
    path('product/<slug:slug>/', geekshop.product_detail, name='product'),
]
