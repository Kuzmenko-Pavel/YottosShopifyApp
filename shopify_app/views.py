import json
import re

import shopify
from django.conf import settings
from django.contrib.messages import get_messages, add_message, INFO
from django.shortcuts import render, redirect
from django.template import RequestContext
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import TemplateResponseMixin, View, TemplateView, HttpResponse

from .helpers import verify_webhook, route_url
from .models import ShopifyStore


def index(request):
    context = {'SHOPIFY_API_SCOPE': settings.SHOPIFY_API_SCOPE, 'request': RequestContext(request)}
    return render(request, 'index.html', context)


def save(request):
    if request.method == 'POST':
        save_type = request.GET.get('type')
        json_data = json.loads(request.body.decode('utf-8'))
        data = json_data.get('data')
        domain = json_data.get('shop')
        feed_name = json_data.get('feed_name', 'fb')
        shop = ShopifyStore.objects.get(myshopify_domain=domain)
        if shop and shop.premium:
            if save_type == 'collections':
                feed_data = shop.feeds.get(feed_name, {'utm': {}, 'collection': []})
                feed_data['collection'] = data
                shop.feeds[feed_name] = feed_data
                shop.save()

            if save_type == 'utm':
                feed_data = shop.feeds.get(feed_name, {'utm': {}, 'collection': []})
                feed_data['utm'] = {i['name']: i['value'] for i in data}
                shop.feeds[feed_name] = feed_data
                shop.save()

    return HttpResponse("OK")


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
            'page_name': 'Your Facebook Feed',
            'title': "Facebook product feed set up!",
            'description': "You have successfully generated your Facebook product feed. You can now add it to your Facebook Catalog.",
            'sectioned_title': "Your Facebook Feed",
            'link': 'facebook',
            'offer_count': 0
        },
        'ga': {
            'page_name': 'Your Google Feed',
            'title': "Google product feed set up!",
            'description': "You have successfully generated your Google product feed. You can now add it to your Google Catalog.",
            'sectioned_title': "Your Google Feed",
            'link': 'google',
            'offer_count': 0
        },
        'yt': {
            'page_name': 'Your Yottos Feed',
            'title': "Yottos product feed set up!",
            'description': "You have successfully generated your Yottos product feed. You can now add it to your Yottos Catalog.",
            'sectioned_title': "Your Yottos Feed",
            'link': 'yottos',
            'offer_count': 0
        },
        'pi': {
            'page_name': 'Your Pinterest Feed',
            'title': "Pinterest product feed set up!",
            'description': "You have successfully generated your Yottos product feed. You can now add it to your Pinterest Catalog.",
            'sectioned_title': "Your Pinterest Feed",
            'link': 'pinterest',
            'offer_count': 0
        },
    }
    utm = [
        {
            'value': 'facebook',
            'label': 'Campaign Source',
            'name': 'cs'
        },
        {
            'value': 'cpc',
            'label': 'Campaign Medium',
            'name': 'cm'
        },
        {
            'value': 'test-yottos.myshopify.com',
            'label': 'Campaign Name',
            'name': 'cn'
        }
    ]

    def get(self, request, *args, **kwargs):
        utm = []
        collection = []
        feed_name = kwargs.get('feed', 'fb')
        premium = False
        storage = get_messages(request)
        for message in storage:
            if message == 'premium_active':
                premium = True
        feed = self.feeds.get(feed_name, self.feeds.get('fb'))
        shop = self.get_shop(request.shop)
        if shop:
            feed_option = shop.feeds.get(feed_name, shop.feeds.get('fb'))
            collection = feed_option.get('collection', [])
            for item in self.utm:
                utm_val = feed_option.get('utm', {}).get(item.get('name'))
                if utm_val:
                    item['value'] = utm_val
                utm.append(item)

        context = {
            'page_name': feed['page_name'],
            'premium': premium,
            'shop': shop,
            'feed': feed,
            'utm': utm,
            'collection': collection,
            'feed_name': feed_name
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
                    coll = [{'name': 'yt__all', 'label': 'All Product', 'value': ('', True)}]
                    collections = shopify.CustomCollection.find()
                    for collection in collections:
                        coll.append({'label': collection.title, 'name': collection.handle})
                    collections = shopify.SmartCollection.find()
                    for collection in collections:
                        coll.append({'label': collection.title, 'name': collection.handle})

                    url = route_url('shopify_app:dashboard', _query=_query)
                    if count:
                        old_coll_fb = {x['name']: (x['label'], x['value']) for x in
                                       shop.feeds.get('fb', {}).get('collection', [])}
                        old_coll_ga = {x['name']: (x['label'], x['value']) for x in
                                       shop.feeds.get('ga', {}).get('collection', [])}
                        old_coll_yt = {x['name']: (x['label'], x['value']) for x in
                                       shop.feeds.get('yt', {}).get('collection', [])}
                        old_coll_pi = {x['name']: (x['label'], x['value']) for x in
                                       shop.feeds.get('pi', {}).get('collection', [])}
                        new_coll_fb = []
                        new_coll_ga = []
                        new_coll_yt = []
                        new_coll_pi = []
                        for c in coll:
                            value = old_coll_fb.get(c['name'], c.get('value', ('', False)))[1]
                            new_coll_fb.append({'value': value, 'label': c['label'], 'name': c['name']})

                            value = old_coll_ga.get(c['name'], c.get('value', ('', False)))[1]
                            new_coll_ga.append({'value': value, 'label': c['label'], 'name': c['name']})

                            value = old_coll_yt.get(c['name'], c.get('value', ('', False)))[1]
                            new_coll_yt.append({'value': value, 'label': c['label'], 'name': c['name']})

                            value = old_coll_pi.get(c['name'], c.get('value', ('', False)))[1]
                            new_coll_pi.append({'value': value, 'label': c['label'], 'name': c['name']})

                        shop.feeds['fb']['collection'] = new_coll_fb
                        shop.feeds['ga']['collection'] = new_coll_ga
                        shop.feeds['yt']['collection'] = new_coll_yt
                        shop.feeds['pi']['collection'] = new_coll_pi
                        shop.offer_count = count
                        shop.save()
            except Exception as e:
                print(e)
        return redirect(url)

    def post(self, request, *args, **kwargs):
        shop = request.GET.get('shop') or request.POST.get('shop')
        _query = {
            'shop': re.sub(r'.*://?([^/?]+).*', '\g<1>', shop)
        }
        url = route_url('shopify_app:authenticate', _query=_query)
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
            feeds = obj.feeds
            feeds['fb']['utm']['cn'] = shop_url
            feeds['ga']['utm']['cn'] = shop_url
            feeds['yt']['utm']['cn'] = shop_url
            feeds['pi']['utm']['cn'] = shop_url
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
                obj.feeds = feeds
                obj.save()
            else:
                if obj.access_token != token:
                    obj.access_token = token
                    obj.installed = True
                    obj.feeds = feeds
                    obj.save()
                if not obj.installed:
                    obj.installed = True
                    obj.feeds = feeds
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
                    rac.price = 29.00
                    rac.trial_days = 60
                    rac.trial_ends_on = timezone.now() + timezone.timedelta(days=60)
                    rac.name = "Premium"
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
        msg = 'premium_not_active'
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
                    msg = 'premium_active'
        add_message(request, INFO, msg)
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
