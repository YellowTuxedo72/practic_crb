from django.db import models
from django.urls import reverse
from django_editorjs_fields import EditorJsJSONField
import re

class News(models.Model):
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    slug = models.SlugField(max_length=200, unique=True, verbose_name="URL")
    
    # НОВОЕ ПОЛЕ: Миниатюра для карточки новости
    thumbnail = models.ImageField(
        upload_to="news_thumbnails/", 
        blank=True, 
        null=True, 
        verbose_name="Миниатюра (Превью)"
    )
    
    text = EditorJsJSONField(verbose_name="Содержимое новости") 
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата")
    is_published = models.BooleanField(default=True, verbose_name="Опубликовано")

    class Meta:
        verbose_name = "Новость"
        verbose_name_plural = "Новости"

    def __str__(self):
        return self.title
    @property
    def preview(self):
        if not self.text:
            return ""

        result = []

        for block in self.text.get("blocks", []):
            text = block.get("data", {}).get("text")
            if text:
                # Убираем HTML-теги
                clean = re.sub(r"<[^>]*>", "", text)
                result.append(clean)

        return " ".join(result)[:80] + "..."


class NavigationSection(models.Model):
    title = models.CharField(
        max_length=100,
        verbose_name="Название",
    )

    order = models.PositiveIntegerField(
        default=0,
        verbose_name="Порядок",
    )

    is_visible = models.BooleanField(
        default=True,
        verbose_name="Показывать в меню",
    )

    class Meta:
        ordering = ["order", "title"]
        verbose_name = "Раздел меню"
        verbose_name_plural = "Разделы меню"

    def __str__(self):
        return self.title


class Page(models.Model):
    title = models.CharField(
        max_length=200,
        verbose_name="Название",
    )

    slug = models.SlugField(
        max_length=200,
        unique=True,
        verbose_name="URL",
    )

    content = EditorJsJSONField(
        verbose_name="Содержимое",
    )

    section = models.ForeignKey(
        NavigationSection,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="pages",
        verbose_name="Раздел меню",
    )

    navigation_order = models.PositiveIntegerField(
        default=0,
        verbose_name="Порядок в разделе",
    )

    is_published = models.BooleanField(
        default=True,
        verbose_name="Опубликовано",
    )

    class Meta:
        ordering = ["navigation_order", "title"]
        verbose_name = "Страница"
        verbose_name_plural = "Страницы"

    def __str__(self):
        return self.title