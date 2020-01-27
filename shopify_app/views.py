import json

import shopify
from django.conf import settings
from django.shortcuts import render, redirect
from django.template import RequestContext
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import TemplateResponseMixin, View, TemplateView

from .helpers import verify_webhook, route_url
from .models import ShopifyStore


def index(request):
    context = {'SHOPIFY_API_SCOPE': settings.SHOPIFY_API_SCOPE, 'request': RequestContext(request)}
    return render(request, 'index.html', context)


class BaseShop(object):

    def get_shop(self, domain):
        try:
            return ShopifyStore.objects.get(myshopify_domain=domain)
        except ShopifyStore.DoesNotExist:
            return None


class Dashboard(TemplateView, BaseShop):
    template_name = "dashboard.html"
    feeds = {
        'fb': {
            'title': "Facebook product feed set up!",
            'description': "You have successfully generated your Facebook product feed. You can now add it to your Facebook Catalog.",
            'sectioned_title': "Your Facebook Feed",
            'link': 'facebook',
            'offer_count': 0
        },
        'ga': {
            'title': "Google product feed set up!",
            'description': "You have successfully generated your Google product feed. You can now add it to your Google Catalog.",
            'sectioned_title': "Your Google Feed",
            'link': 'google',
            'offer_count': 0
        },
        'yt': {
            'title': "Facebook product feed set up!",
            'description': "You have successfully generated your Yottos product feed. You can now add it to your Yottos Catalog.",
            'sectioned_title': "Your Yottos Feed",
            'link': 'yottos',
            'offer_count': 0
        },
        'pi': {
            'title': "Facebook product feed set up!",
            'description': "You have successfully generated your Yottos product feed. You can now add it to your Pinterest Catalog.",
            'sectioned_title': "Your Pinterest Feed",
            'link': 'pinterest',
            'offer_count': 0
        },
    }

    def get(self, request, *args, **kwargs):
        feed_name = request.GET.get('feed', 'fb')
        feed = self.feeds.get(feed_name, self.feeds.get('fb'))

        context = {
            'page_name': 'Your Feed',
            'shop': self.get_shop(request.shop),
            'feed': feed
        }

        return self.render_to_response(context)


class Authenticate(View, BaseShop):

    def get(self, request, *args, **kwargs):
        shop = self.get_shop(request.shop)
        _query = {
            'shop': request.shop, 'hmac': request.hmac, 'timestamp': request.timestamp
        }
        url = route_url('shopify_app:install', _query=_query)
        if shop and shop.installed:
            try:
                with shopify.Session.temp(shop.myshopify_domain, settings.SHOPIFY_API_VERSION, shop.access_token):
                    count = shopify.Product.count()
                    url = route_url('shopify_app:dashboard', _query=_query)
                    if count:
                        shop.offer_count = count
                        shop.save()
            except Exception as e:
                print(e)
        return redirect(url)


class Install(View):

    def get(self, request, *args, **kwargs):
        shop = request.shop
        _query = {
            'shop': request.shop, 'hmac': request.hmac, 'timestamp': request.timestamp
        }
        if shop:
            scope = settings.SHOPIFY_API_SCOPE
            redirect_uri = request.build_absolute_uri(route_url('shopify_app:finalize'))
            session = shopify.Session(shop.strip(), settings.SHOPIFY_API_VERSION)
            url = session.create_permission_url(scope, redirect_uri)
        else:
            url = route_url('shopify_app:index', _query=_query)
            url = request.build_absolute_uri(url)
        return redirect(url)


class Finalize(View):

    def create_shopify_store(self, shop_url, token):
        with shopify.Session.temp(shop_url, settings.SHOPIFY_API_VERSION, token):
            obj, created = ShopifyStore.objects.get_or_create(myshopify_domain=shop_url)
            if created:
                shop = shopify.Shop.current()
                count = shopify.Product.count()
                obj.myshopify_domain = shop.myshopify_domain
                obj.access_token = token
                obj.date_installed = timezone.now()
                obj.email = shop.email
                obj.shop_owner = shop.shop_owner
                obj.country_name = shop.country_name
                obj.name = shop.name
                obj.installed = True
                if count:
                    shop.offer_count = count
                obj.save()
            else:
                if obj.access_token != token:
                    obj.access_token = token
                    obj.installed = True
                    obj.save()
                if not obj.installed:
                    obj.installed = True
                    obj.save()

    def webhook_create(self, request, shop_url, token):
        with shopify.Session.temp(shop_url, settings.SHOPIFY_API_VERSION, token):
            webhook_data = {
                "topic": 'app/uninstalled',
                "address": request.build_absolute_uri(route_url('shopify_app:app_uninstalled')),
                "format": "json"
            }
            webhook = shopify.Webhook()
            w = webhook.create(webhook_data)

    def get(self, request, *args, **kwargs):
        shop = request.shop
        _query = {
            'shop': request.shop, 'hmac': request.hmac, 'timestamp': request.timestamp
        }
        url = route_url('shopify_app:dashboard', _query=_query)
        try:
            shopify_session = shopify.Session(shop, settings.SHOPIFY_API_VERSION)
            access_token = shopify_session.request_token(request.GET)
            self.create_shopify_store(shop, access_token)
            self.webhook_create(request, shop, access_token)
        except Exception:
            url = route_url('shopify_app:authenticate', _query=_query)
        return redirect(url)


class Subscribe(TemplateView, BaseShop):
    template_name = "subscribe.html"

    def get(self, request, *args, **kwargs):
        _query = {
            'shop': request.shop, 'hmac': request.hmac, 'timestamp': request.timestamp
        }
        context = {'url': route_url('shopify_app:authenticate', _query=_query)}
        try:
            shop = self.get_shop(request.shop)
            if shop:
                with shopify.Session.temp(shop.myshopify_domain, settings.SHOPIFY_API_VERSION, shop.access_token):
                    rac = shopify.RecurringApplicationCharge()
                    rac.test = True
                    rac.return_url = request.build_absolute_uri(
                        route_url('shopify_app:subscribe_submit', _query=_query))
                    rac.price = 10.00
                    rac.name = "Test name"
                    if rac.save():
                        context['url'] = rac.confirmation_url

        except Exception as e:
            print(e)
        return self.render_to_response(context)


class SubmitSubscribe(View, BaseShop):

    def get(self, request, *args, **kwargs):
        _query = {
            'shop': request.shop, 'hmac': request.hmac, 'timestamp': request.timestamp
        }
        charge_id = request.GET.get('charge_id')
        shop = self.get_shop(request.shop)
        if shop and charge_id:
            with shopify.Session.temp(shop.myshopify_domain, settings.SHOPIFY_API_VERSION, shop.access_token):
                rac = shopify.RecurringApplicationCharge.find(charge_id)
                rac.activate()
                if rac.status == 'active':
                    shop.premium = True
                    shop.date_paid = timezone.now()
                    shop.save()
        url = request.build_absolute_uri(route_url('shopify_app:dashboard', _query=_query))
        return redirect(url)


@method_decorator(csrf_exempt, name='dispatch')
class WebhookAppUninstalled(TemplateView, BaseShop):
    template_name = "webhook.html"

    def post(self, request, *args, **kwargs):
        if request.method == 'POST' and verify_webhook(request.body, request.headers.get('X-Shopify-Hmac-Sha256')):
            topic = request.headers.get('X-Shopify-Topic')
            shop_url = request.headers.get('X-Shopify-Shop-Domain')
            data = json.loads(request.body.decode('utf-8'))
            if topic == 'app/uninstalled':
                shop = self.get_shop(shop_url)
                if shop:
                    shop.installed = False
                    shop.premium = False
                    shop.date_uninstalled = timezone.now()
                    shop.save()

        return self.render_to_response({})


class MainXml(TemplateResponseMixin, View, BaseShop):
    template_name = "liquid/main.liquid"
    content_type = 'application/liquid'

    def get(self, request, *args, **kwargs):
        context = {
            'shop': self.get_shop(request.shop),
            'page': int(request.GET.get('page', '1'))
        }
        return self.render_to_response(context)

    def render_to_response(self, context, **response_kwargs):
        """
        Return a response, using the `response_class` for this view, with a
        template rendered with the given context.

        Pass response_kwargs to the constructor of the response class.
        """
        response_kwargs.setdefault('content_type', self.content_type)
        shop = context.get('shop')
        page = context.get('page', 1)
        template = self.get_template_names()
        if shop is None:
            template = ["liquid/main.liquid"]
        else:
            if page > 1 and not shop.premium:
                template = ["liquid/main.liquid"]
        return self.response_class(
            request=self.request,
            template=template,
            context=context,
            using=self.template_engine,
            **response_kwargs
        )

    def head(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)


class GoogleXml(MainXml):
    template_name = "liquid/ga_feed.liquid"


class FacebookXml(MainXml):
    template_name = "liquid/fb_feed.liquid"


class YottosXml(MainXml):
    template_name = "liquid/yt_feed.liquid"


class PinterestXml(MainXml):
    template_name = "liquid/pi_feed.liquid"
