from django.contrib import admin

from geekshop.models import Product, ProductCategory


class ProductCategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(ProductCategory, ProductCategoryAdmin)

admin.site.register(Product)
