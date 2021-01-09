from django.views.generic.base import TemplateView
from facebook_app.tasks import fb_test_call_api


class Index(TemplateView):
    template_name = "facebook_app/index.html"


class TestRun(TemplateView):
    template_name = "facebook_app/test.html"

    def render_to_response(self, *args, **kwargs):
        fb_test_call_api.apply_async((), countdown=10)
        return super(TestRun, self).render_to_response(*args, **kwargs)
