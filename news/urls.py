from django.urls import path

from news import views as news

app_name = 'news'

urlpatterns = [
    path('', news.news, name='news'),
    path('<slug:slug>', news.article, name='article'),
]
