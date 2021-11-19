from django.views.generic import DetailView, ListView

from adminapp.views.mixins import CallableMixin
from basket.views import BasketMixin
from news.models import Article


class NewsList(CallableMixin, BasketMixin, ListView):
    queryset = Article.objects.filter(is_published=True)
    context_object_name = 'articles'
    template_name = 'news/news.html'


class ArticleDetail(CallableMixin, BasketMixin, DetailView):
    model = Article
    context_object_name = 'article'
    template_name = 'news/article.html'


# алиасы
news = NewsList.as_view()
article = ArticleDetail.as_view()
