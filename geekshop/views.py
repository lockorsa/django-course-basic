from django.shortcuts import render


def index(request):
    return render(request, 'geekshop/index.html')


def products(request):
    return render(request, 'geekshop/products.html')


def contact(request):
    return render(request, 'geekshop/contact.html')
