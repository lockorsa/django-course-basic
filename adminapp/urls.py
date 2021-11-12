from django.urls import path
from adminapp import views as adminapp_views

app_name = 'adminapp'

urlpatterns = [
    path('', adminapp_views.admin, name='admin'),
    path('user/', adminapp_views.users, name='users'),
    path('user/create/', adminapp_views.user_create, name='user_create'),
    path('user/update/<int:pk>/', adminapp_views.user_update, name='user_update'),
    path('user/delete/<int:pk>/', adminapp_views.user_delete, name='user_delete'),

    path('categories/', adminapp_views.categories, name='categories'),
    path('category/create/', adminapp_views.category_create, name='category_create'),
    path('category/update/<int:pk>/', adminapp_views.category_update, name='category_update'),
    path('category/delete/<int:pk>/', adminapp_views.category_delete, name='category_delete'),
    
    path('products/<int:pk>/', adminapp_views.products, name='products'),
    path('product/create/<int:pk>/', adminapp_views.product_create, name='product_create'),
    path('product/detail/<int:pk>/', adminapp_views.product_detail, name='product_detail'),
    path('product/update/<int:pk>/', adminapp_views.product_update, name='product_update'),
    path('product/delete/<int:pk>/', adminapp_views.product_delete, name='product_delete'),
]
