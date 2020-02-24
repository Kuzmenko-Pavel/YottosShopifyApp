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


class FAQ(TemplateView):
    template_name = "faq.html"

    def get(self, request, *args, **kwargs):
        context = {}
        return self.render_to_response(context)


class HowInstall(TemplateView):
    template_name = "how_install.html"

    def get(self, request, *args, **kwargs):
        context = {}
        return self.render_to_response(context)


class HowConfigure(TemplateView):
    template_name = "how_configure.html"

    def get(self, request, *args, **kwargs):
        context = {}
        return self.render_to_response(context)


class HowSetupGoogle(TemplateView):
    template_name = "how_setup_google.html"

    def get(self, request, *args, **kwargs):
        context = {}
        return self.render_to_response(context)


class HowSetupFacebook(TemplateView):
    template_name = "how_setup_facebook.html"

    def get(self, request, *args, **kwargs):
        context = {}
        return self.render_to_response(context)


class HowSetupInstagram(TemplateView):
    template_name = "how_setup_instagram.html"

    def get(self, request, *args, **kwargs):
        context = {}
        return self.render_to_response(context)


class HowSetupYottos(TemplateView):
    template_name = "how_setup_yottos.html"

    def get(self, request, *args, **kwargs):
        context = {}
        return self.render_to_response(context)


class HowSetupPinterest(TemplateView):
    template_name = "how_setup_pinterest.html"

    def get(self, request, *args, **kwargs):
        context = {}
        return self.render_to_response(context)
