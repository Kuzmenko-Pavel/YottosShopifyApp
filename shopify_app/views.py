from django.shortcuts import render, redirect
from django.conf import settings
import shopify
import json
from django.template import RequestContext
from django.urls import reverse

from django.utils import timezone
from .helpers import verify_webhook, ShopifyHelper
from . import tasks


def index(request):
    context = {'SHOPIFY_API_SCOPE': settings.SHOPIFY_API_SCOPE, 'request': RequestContext(request)}
    return render(request, 'index.html', context)


def install(request):
    return render(request, 'login.html')


def authenticate(request):
    shop = request.GET.get('shop') or request.POST.get('shop')
    if shop:
        scope = settings.SHOPIFY_API_SCOPE
        redirect_uri = request.build_absolute_uri(reverse('shopify_app:finalize'))
        print(redirect_uri)
        permission_url = shopify.Session(shop.strip(), settings.SHOPIFY_API_VERSION).create_permission_url(scope, redirect_uri)
        return redirect(permission_url)

    return redirect(_return_address(request))


def _return_address(request):
    return request.session.get('return_to') or reverse('home:index')


def finalize(request):
    shop_url = request.GET.get('shop')
    try:
        shopify_session = shopify.Session(shop_url, settings.SHOPIFY_API_VERSION)
        request.session['shopify'] = {
            "shop_url": shop_url,
            "access_token": shopify_session.request_token(request.GET)
        }
        # create_shopify_store_user(request.session['shopify'])
    except Exception:
        # messages.error(request, "Could not log in to Shopify store.")
        return redirect(reverse('shopify_app:login'))

    # messages.info(request, "Logged in to shopify store.")
    response = redirect(_return_address(request))
    # request.session.pop('return_to', None)
    return response


def webhook_app_uninstalled(request):
    if request.method == 'POST' and verify_webhook(request.body, request.headers.get('X-Shopify-Hmac-Sha256')):
        topic = request.headers.get('X-Shopify-Topic')
        shop_url = request.headers.get('X-Shopify-Shop-Domain')
        data = json.loads(request.body)
        data.update({'X-Shopify-Shop-Domain': shop_url})
        if topic == 'app/uninstalled':
            tasks.app_uninstalled(data, verbose_name='Task for app/uninstalled webhook event: %s' % shop_url)
    return render(request, 'webhook.html')
