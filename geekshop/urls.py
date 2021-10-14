from django.urls import path

from geekshop import views

urlpatterns = [
    path('', views.index),
    path('products/', views.products),
    path('contact/', views.contact),
]
