from django.views.generic.base import TemplateView


class Index(TemplateView):
    template_name = "index.html"

    def get(self, request, *args, **kwargs):
        context = {}
        return self.render_to_response(context)


class Privacy(TemplateView):
    template_name = "privacy.html"

    def get(self, request, *args, **kwargs):
        context = {}
        return self.render_to_response(context)


class Cookie(TemplateView):
    template_name = "cookie-policy.html"

    def get(self, request, *args, **kwargs):
        context = {}
        return self.render_to_response(context)
