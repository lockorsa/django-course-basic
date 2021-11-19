from django.urls import path

from adminapp.views import create_views, delete_views, read_views, update_views

app_name = 'adminapp'

urlpatterns = [
    # read
    path('', read_views.admin, name='admin'),
    path('users/', read_views.users, name='users'),
    path('categories/', read_views.categories, name='categories'),
    path('products/<int:pk>/', read_views.products, name='products'),
    path('product/detail/<int:pk>/', read_views.product_detail, name='product_detail'),

    # create
    path('user/create/', create_views.user_create, name='user_create'),
    path('category/create/', create_views.category_create, name='category_create'),
    path('product/create/<int:pk>/', create_views.product_create, name='product_create'),

    # update
    path('user/update/<int:pk>/', update_views.user_update, name='user_update'),
    path('category/update/<int:pk>/', update_views.category_update, name='category_update'),
    path('product/update/<int:pk>/', update_views.product_update, name='product_update'),

    # delete
    path('user/delete/<int:pk>/', delete_views.user_delete, name='user_delete'),    
    path('category/delete/<int:pk>/', delete_views.category_delete, name='category_delete'),
    path('product/delete/<int:pk>/', delete_views.product_delete, name='product_delete'),
]
