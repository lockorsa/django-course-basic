from django.shortcuts import render, HttpResponseRedirect, reverse


def basket(request):
    return HttpResponseRedirect(reverse('index'))


def add(request):
    pass


def remove(request):
    pass
