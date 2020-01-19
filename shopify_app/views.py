from django.shortcuts import render, redirect
from django.conf import settings
import shopify
import json
from django.template import RequestContext
from django.views.generic.base import TemplateResponseMixin, View, TemplateView

from django.utils import timezone
from .helpers import verify_webhook, ShopifyHelper, route_url
from . import tasks


def index(request):
    context = {'SHOPIFY_API_SCOPE': settings.SHOPIFY_API_SCOPE, 'request': RequestContext(request)}
    return render(request, 'index.html', context)


class Dashboard(TemplateView):
    template_name = "dashboard.html"

    def get(self, request, *args, **kwargs):
        context = {'page_name': 'Home'}

        return self.render_to_response(context)


class Authenticate(View):

    def get(self, request, *args, **kwargs):
        shop = request.GET.get('shop')
        hmac = request.GET.get('hmac')
        timestamp = request.GET.get('timestamp')
        if shop:
            url = route_url('shopify_app:install', _query={'shop': shop, 'hmac': hmac, 'timestamp': timestamp})
        else:
            url = route_url('shopify_app:dashboard', _query={'shop': shop, 'hmac': hmac, 'timestamp': timestamp})

        return redirect(url)


class Install(View):

    def get(self, request, *args, **kwargs):
        shop = request.GET.get('shop')
        hmac = request.GET.get('hmac')
        timestamp = request.GET.get('timestamp')
        if shop:
            scope = settings.SHOPIFY_API_SCOPE
            redirect_uri = request.build_absolute_uri(route_url('shopify_app:finalize'))
            session = shopify.Session(shop.strip(), settings.SHOPIFY_API_VERSION)
            url = session.create_permission_url(scope, redirect_uri)
        else:
            url = route_url('shopify_app:index', _query={'shop': shop, 'hmac': hmac, 'timestamp': timestamp})
            url = request.build_absolute_uri(url)
        return redirect(url)


class Finalize(View):

    def get(self, request, *args, **kwargs):
        shop = request.GET.get('shop')
        hmac = request.GET.get('hmac')
        timestamp = request.GET.get('timestamp')
        url = route_url('shopify_app:dashboard', _query={'shop': shop, 'hmac': hmac, 'timestamp': timestamp})
        try:
            shopify_session = shopify.Session(shop, settings.SHOPIFY_API_VERSION)
            access_token = shopify_session.request_token(request.GET)
            print(access_token)
        except Exception:
            url = route_url('shopify_app:authenticate', _query={'shop': shop, 'hmac': hmac, 'timestamp': timestamp})
        return redirect(url)


class WebhookAppUninstalled(TemplateView):
    template_name = "webhook.html"

    def post(self, request, *args, **kwargs):
        if request.method == 'POST' and verify_webhook(request.body, request.headers.get('X-Shopify-Hmac-Sha256')):
            topic = request.headers.get('X-Shopify-Topic')
            shop_url = request.headers.get('X-Shopify-Shop-Domain')
            data = json.loads(request.body)
            data.update({'X-Shopify-Shop-Domain': shop_url})
            if topic == 'app/uninstalled':
                tasks.app_uninstalled(data, verbose_name='Task for app/uninstalled webhook event: %s' % shop_url)
        return self.render_to_response({})


class MainXml(TemplateResponseMixin, View):
    template_name = "liquid/main.liquid"
    content_type = 'application/liquid'

    def get(self, request, *args, **kwargs):
        context = {}
        return self.render_to_response(context)

    def head(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)


class GoogleXml(TemplateResponseMixin, View):
    template_name = "liquid/ga_feed.liquid"
    content_type = 'application/liquid'

    def get(self, request, *args, **kwargs):
        context = {}
        return self.render_to_response(context)

    def head(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)


class FacebookXml(TemplateResponseMixin, View):
    template_name = "liquid/fb_feed.liquid"
    content_type = 'application/liquid'

    def get(self, request, *args, **kwargs):
        context = {}
        return self.render_to_response(context)

    def head(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)


class YottosXml(TemplateResponseMixin, View):
    template_name = "liquid/yt_feed.liquid"
    content_type = 'application/liquid'

    def get(self, request, *args, **kwargs):
        context = {}
        return self.render_to_response(context)

    def head(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)
