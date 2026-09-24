from .models import NavigationSection


def navigation_sections(request):
    sections = (
        NavigationSection.objects
        .filter(is_visible=True)
        .prefetch_related("pages")
        .order_by("order", "title")
    )

    return {
        "navigation_sections": sections,
    }