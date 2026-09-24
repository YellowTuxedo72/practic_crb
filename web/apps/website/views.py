from django.shortcuts import render
from .models import News
from django.shortcuts import get_object_or_404, render
from .models import Page
from django.shortcuts import render
from .models import News


def index(request):
    news_list = News.objects.filter(
        is_published=True
    ).order_by("-created_at")[:3]

    context = {
        "news_list": news_list,
    }

    return render(request, "website/index.html", context)


def news_view(request):
    news_list = News.objects.filter(
        is_published=True
    ).order_by("-created_at")

    return render(
        request,
        "website/news.html",
        {
            "news_list": news_list,
        },
    )
    
def news_detail(request, slug):
    news = get_object_or_404(
        News,
        slug=slug,
        is_published=True,
    )

    return render(
        request,
        "website/news_detail.html",
        {
            "news": news,
        },
    )

def test_news_view(request):
    """Тестовая страница для проверки вывода блоков Editor.js"""
    # Берем самую последнюю добавленную новость из базы данных
    latest_news = News.objects.filter(is_published=True).first()
    
    context = {
        'news': latest_news
    }
    return render(request, 'website/test_news.html', context)



def page_detail(request, slug):
    page = get_object_or_404(
        Page,
        slug=slug,
        is_published=True,
    )

    return render(
        request,
        "website/page.html",
        {
            "page": page,
        }
    )