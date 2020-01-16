from django.shortcuts import render, redirect
from django.conf import settings
import shopify
import json
from django.template import RequestContext
from django.views.generic.base import TemplateResponseMixin, View
from django.urls import reverse

from django.utils import timezone
from .helpers import verify_webhook, ShopifyHelper
from . import tasks


def index(request):
    print(request.GET)
    print(request.POST)
    print(request.META)
    context = {'SHOPIFY_API_SCOPE': settings.SHOPIFY_API_SCOPE, 'request': RequestContext(request)}
    return render(request, 'index.html', context)


def dashboard(request):
    print(request.GET)
    print(request.POST)
    print(request.META)
    context = {'SHOPIFY_API_SCOPE': settings.SHOPIFY_API_SCOPE, 'request': RequestContext(request)}
    return render(request, 'index.html', context)


def install(request):
    print(request.GET)
    print(request.POST)
    print(request.META)
    shop = request.GET.get('shop') or request.POST.get('shop')
    if shop:
        scope = settings.SHOPIFY_API_SCOPE
        redirect_uri = request.build_absolute_uri(reverse('shopify_app:finalize'))
        print(redirect_uri)
        permission_url = shopify.Session(shop.strip(), settings.SHOPIFY_API_VERSION).create_permission_url(scope,
                                                                                                           redirect_uri)
        return redirect(permission_url)
    url = reverse('shopify_app:index')
    qs = '&'.join(['shop', shop])
    url = '?'.join((url, qs))
    return redirect(url)


def authenticate(request):
    print(request.GET)
    print(request.POST)
    print(request.META)
    shop = request.GET.get('shop') or request.POST.get('shop')
    if shop:
        url = reverse('shopify_app:install')
    else:
        url = reverse('shopify_app:dashboard')

    qs = '&'.join(['shop', shop])
    url = '?'.join((url, qs))
    return redirect(url)


def finalize(request):
    print(request.GET)
    print(request.POST)
    print(request.META)
    shop = request.GET.get('shop') or request.POST.get('shop')
    url = reverse('shopify_app:dashboard')
    try:
        shopify_session = shopify.Session(shop, settings.SHOPIFY_API_VERSION)
        request.session['shopify'] = {
            "shop_url": shop,
            "access_token": shopify_session.request_token(request.GET)
        }
    except Exception:
        url = reverse('shopify_app:authenticate')

    qs = '&'.join(['shop', shop])
    url = '?'.join((url, qs))
    return redirect(url)


def webhook_app_uninstalled(request):
    if request.method == 'POST' and verify_webhook(request.body, request.headers.get('X-Shopify-Hmac-Sha256')):
        topic = request.headers.get('X-Shopify-Topic')
        shop_url = request.headers.get('X-Shopify-Shop-Domain')
        data = json.loads(request.body)
        data.update({'X-Shopify-Shop-Domain': shop_url})
        if topic == 'app/uninstalled':
            tasks.app_uninstalled(data, verbose_name='Task for app/uninstalled webhook event: %s' % shop_url)
    return render(request, 'webhook.html')


class GoogleXml(TemplateResponseMixin, View):
    template_name = "liquid/ga_feed.liquid"
    content_type = 'application/liquid'

    def get(self, request, *args, **kwargs):
        print(request.GET)
        print(request.POST)
        print(request.META)
        context = {}
        return self.render_to_response(context)

    def head(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)


class FacebookXml(TemplateResponseMixin, View):
    template_name = "liquid/fb_feed.liquid"
    content_type = 'application/liquid'

    def get(self, request, *args, **kwargs):
        print(request.GET)
        print(request.POST)
        print(request.META)
        context = {}
        return self.render_to_response(context)

    def head(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)


class YottosXml(TemplateResponseMixin, View):
    template_name = "liquid/yt_feed.liquid"
    content_type = 'application/liquid'

    def get(self, request, *args, **kwargs):
        print(request.GET)
        print(request.POST)
        print(request.META)
        context = {}
        return self.render_to_response(context)

    def head(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)
