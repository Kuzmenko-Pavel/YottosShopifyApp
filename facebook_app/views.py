from django.views.generic.base import TemplateView


class Index(TemplateView):
    template_name = "facebook_app/index.html"
