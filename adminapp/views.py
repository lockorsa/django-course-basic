from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import get_object_or_404, HttpResponseRedirect, render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import ListView, TemplateView

from adminapp.forms import ShopUserAdminEditForm
from authapp.forms import ShopUserRegisterForm
from authapp.models import ShopUser
from geekshop.forms import CategoryForm, ProductForm
from geekshop.models import Category, Product


class AccessMixin:
    @method_decorator(user_passes_test(lambda user: user.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class AdminIndex(AccessMixin, TemplateView):
    template_name = 'adminapp/admin.html'


class UserList(AccessMixin, ListView):
    model = ShopUser
    ordering = ['-is_active']
    template_name = 'adminapp/users.html'


class CategoryList(AccessMixin, ListView):
    model = Category
    ordering = ['-is_active']
    template_name = 'adminapp/categories.html'


class ProductList(AccessMixin, ListView):
    model = Product
    ordering = ['-is_active']
    template_name = 'adminapp/products.html'

    def get_queryset(self, *args, **kwargs):
        """Фильтруем продукты по принадлежности к выбранной категории."""
        queryset = super().get_queryset(*args, **kwargs)
        return queryset.filter(categories__pk=self.kwargs.get('pk'))

    def get_context_data(self, *args, **kwargs):
        """Добавляем в контекст необходимый объект категории."""
        context = super().get_context_data(*args, **kwargs)
        context['category'] = get_object_or_404(
            Category,
            pk=self.kwargs.get('pk'),
        )
        return context


@user_passes_test(lambda user: user.is_superuser)
def user_create(request):
    if request.method == 'POST':
        user_form = ShopUserRegisterForm(request.POST, request.FILES)

        if user_form.is_valid():
            user_form.save()
            return HttpResponseRedirect(reverse('adminapp:users'))
    else:
        user_form = ShopUserRegisterForm()
    context = {
        'form': user_form,
    }
    return render(request, 'adminapp/form.html', context=context)


@user_passes_test(lambda user: user.is_superuser)
def user_update(request, pk: int):
    current_user = get_object_or_404(ShopUser, pk=pk)

    if request.method == 'POST':
        user_form = ShopUserAdminEditForm(
            request.POST,
            request.FILES,
            instance=current_user,
        )

        if user_form.is_valid():
            user_form.save()
            return HttpResponseRedirect(reverse('adminapp:users'))
    else:
        user_form = ShopUserAdminEditForm(instance=current_user)
    context = {
        'form': user_form,
    }
    return render(request, 'adminapp/form.html', context=context)


@user_passes_test(lambda user: user.is_superuser)
def user_delete(request, pk: int):
    current_user = get_object_or_404(ShopUser, pk=pk)
    if request.method == 'POST':
        current_user.is_active = not current_user.is_active
        current_user.save()
        return HttpResponseRedirect(reverse('adminapp:users'))
    context = {
        'object': current_user,
    }
    return render(request, 'adminapp/delete_confirm.html', context=context)


@user_passes_test(lambda user: user.is_superuser)
def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('adminapp:categories'))
    else:
        form = CategoryForm()
    context = {
        'form': form,
    }
    return render(request, 'adminapp/form.html', context=context)


@user_passes_test(lambda user: user.is_superuser)
def category_update(request, pk: int):
    current_category = get_object_or_404(Category, pk=pk)

    if request.method == 'POST':
        category_form = CategoryForm(
            request.POST,
            request.FILES,
            instance=current_category,
        )
        if category_form.is_valid():
            category_form.save()
            return HttpResponseRedirect(reverse('adminapp:categories'))
    else:
        category_form = CategoryForm(instance=current_category)
    context = {
        'form': category_form,
    }
    return render(request, 'adminapp/form.html', context=context)


@user_passes_test(lambda user: user.is_superuser)
def category_delete(request, pk: int):
    current_category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        current_category.is_active = not current_category.is_active
        current_category.save()
        return HttpResponseRedirect(reverse('adminapp:categories'))
    context = {
        'object': current_category,
    }
    return render(request, 'adminapp/delete_confirm.html', context=context)


@user_passes_test(lambda user: user.is_superuser)
def product_create(request, pk: int):
    current_category = get_object_or_404(Category, pk=pk)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            new_product = form.save()
            current_category.products.add(new_product)
            current_category.save()
            return HttpResponseRedirect(reverse(
                'adminapp:proucts',
                kwargs={'pk': pk},
            ))
    else:
        form = ProductForm()
    context = {
        'form': form,
    }
    return render(request, 'adminapp/form.html', context=context)


@user_passes_test(lambda user: user.is_superuser)
def product_update(request, pk: int):
    current_product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(
            request.POST,
            request.FILES,
            instance=current_product,
        )
        if form.is_valid():
            form.save()
            category_pk = current_product.categories.first().pk
            return HttpResponseRedirect(reverse(
                'adminapp:products',
                kwargs={'pk': category_pk},
            ))
    else:
        form = ProductForm(instance=current_product)
    context = {
        'form': form,
    }
    return render(request, 'adminapp/form.html', context=context)


@user_passes_test(lambda user: user.is_superuser)
def product_delete(request, pk: int):
    current_object = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        current_object.is_active = not current_object.is_active
        current_object.save()
        category_pk = current_object.categories.first().pk
        return HttpResponseRedirect(reverse(
            'adminapp:products',
            kwargs={'pk': category_pk},
        ))
    context = {
        'object': current_object,
    }
    return render(request, 'adminapp/delete_confirm.html', context=context)


@user_passes_test(lambda user: user.is_superuser)
def product_detail(request, pk: int):
    current_product = get_object_or_404(Product, pk=pk)
    return HttpResponseRedirect(reverse('geekshop:product', kwargs={
        'slug': current_product.slug,
    }))
