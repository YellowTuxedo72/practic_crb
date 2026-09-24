from django.urls import path
from . import views

app_name = 'website'

urlpatterns = [
    path('', views.index, name='index'),
    path('news/', views.news_view, name='news_page'),
    path(
    "news/<slug:slug>/",
    views.news_detail,
    name="news_detail",
),
    # Наша новая тестовая страница
    path('test-news/', views.test_news_view, name='test_news'), 
    path(
    "pages/<slug:slug>/",
    views.page_detail,
    name="page_detail",
),
]
