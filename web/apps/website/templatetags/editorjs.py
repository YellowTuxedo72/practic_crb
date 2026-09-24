from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def render_editorjs(content):
    if not content:
        return ""

    blocks = content.get("blocks", [])
    result = []

    for block in blocks:
        block_type = block.get("type")
        data = block.get("data", {})

        # Обычный текст
        if block_type == "paragraph":
            text = data.get("text", "")
            if text:
                result.append(
                    f'<p class="page-paragraph">{text}</p>'
                )

        # Таблица
        elif block_type == "Table":
            rows = data.get("content", [])

            if rows:
                table_html = ['<div class="page-table-wrapper">']
                table_html.append('<table class="page-table">')

                for row in rows:
                    table_html.append("<tr>")

                    for cell in row:
                        table_html.append(
                            f"<td>{cell}</td>"
                        )

                    table_html.append("</tr>")

                table_html.append("</table>")
                table_html.append("</div>")

                result.append("".join(table_html))

        # HTML-код / iframe через Code Tool
        elif block_type == "Code":
            code = data.get("code", "")

            if code:
                result.append(
                    f'<div class="page-code">{code}</div>'
                )

    return mark_safe("".join(result))