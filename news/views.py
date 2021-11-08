from django.shortcuts import render, get_object_or_404

from news.models import Article


def news(request):
    context = {
        'articles': Article.objects.filter(is_published=True),
    }
    return render(request, 'news/news.html', context=context)


def article(request, slug):
    context = {
        'article': get_object_or_404(Article, slug=slug),
    }
    return render(request, 'news/article.html', context=context)
