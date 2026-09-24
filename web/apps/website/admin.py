from django.contrib import admin
from .models import News, Page, NavigationSection
from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html, format_html_join


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "section",
        "navigation_order",
        "is_published",
    )

    list_display_links = (
        "title",
    )

    list_filter = (
        "section",
        "is_published",
    )

    search_fields = (
        "title",
        "slug",
    )

    prepopulated_fields = {
        "slug": ("title",)
    }

    list_editable = (
        "navigation_order",
        "is_published",
    )

    ordering = (
        "section",
        "navigation_order",
        "title",
    )

    fieldsets = (
        (
            "Основная информация",
            {
                "fields": (
                    "title",
                    "slug",
                    "content",
                ),
            },
        ),
        (
            "Навигация",
            {
                "fields": (
                    "section",
                    "navigation_order",
                ),
                "description": (
                    "Определяет, в каком разделе меню будет "
                    "находиться страница и в каком порядке она будет отображаться."
                ),
            },
        ),
        (
            "Публикация",
            {
                "fields": (
                    "is_published",
                ),
            },
        ),
    )
    
class PageInline(admin.TabularInline):
    model = Page
    fields = (
        "title",
        "slug",
        "navigation_order",
        "is_published",
    )
    readonly_fields = (
        "title",
        "slug",
        "navigation_order",
        "is_published",
    )
    extra = 0
    can_delete = False
    show_change_link = True    

@admin.register(NavigationSection)
class NavigationSectionAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "pages_count",
        "order",
        "is_visible",
    )

    list_display_links = ("title",)

    list_filter = ("is_visible",)
    search_fields = ("title",)
    ordering = ("order", "title")

    inlines = [PageInline]

    def pages_count(self, obj):
        return obj.pages.filter(is_published=True).count()

    pages_count.short_description = "Опубликованных страниц"
    
