from django.views.generic.base import HttpResponse, View


class Index(View):
    template_name = "dashboard.html"

    def get(self, request, *args, **kwargs):
        response = HttpResponse()
        return response
