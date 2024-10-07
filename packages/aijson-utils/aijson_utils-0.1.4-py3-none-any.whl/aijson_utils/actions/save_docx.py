from aijson import register_action


@register_action
def save_markdown_to_docx(md: str):
    import markdown
    from docx import Document

    html = markdown.markdown(md)
    doc = Document()
    doc.add_paragraph(html)
    doc.save("output.docx")
    return "output.docx"
