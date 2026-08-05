from django.template.loader import render_to_string
from weasyprint import HTML

class PDFService:
    @staticmethod
    def render_pdf(template_name, context):
        """
        Render a PDF for the given Sale instance.
        """
        html = render_to_string(template_name, context)
        pdf_content = HTML(string=html).write_pdf()
        return pdf_content