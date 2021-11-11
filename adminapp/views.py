from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import get_object_or_404, HttpResponseRedirect, render
from django.urls import reverse

from adminapp.forms import ShopUserAdminEditForm
from authapp.forms import ShopUserRegisterForm
from authapp.models import ShopUser
from geekshop.forms import CategoryForm, ProductForm
from geekshop.models import Category, Product


@user_passes_test(lambda user: user.is_superuser)
def admin(request):
    return render(request, 'adminapp/admin.html')


@user_passes_test(lambda user: user.is_superuser)
def users(request):
    context = {
        'object_list': ShopUser.objects.all().order_by('-is_active'),
    }
    return render(request, 'adminapp/users.html', context=context)


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
def categories(request):
    context = {
        'object_list': Category.objects.all().order_by('-is_active'),
    }
    return render(request, 'adminapp/categories.html', context=context)


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
def products(request, pk: int):
    context = {
        'category': get_object_or_404(Category, pk=pk),
        'object_list': Product.objects.filter(categories__pk=pk).order_by('-is_active'),
    }
    return render(request, 'adminapp/products.html', context=context)


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
