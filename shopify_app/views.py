import json
import re
from datetime import datetime

import shopify
from django.conf import settings
from django.contrib.messages import get_messages, add_message, INFO
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.template import RequestContext
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import TemplateResponseMixin, View, TemplateView, HttpResponse

from facebook_app.models import FacebookBusinessManager, FacebookCampaign
from facebook_app.tasks import fb_create_update
from .helpers import verify_webhook, route_url
from .models import ShopifyStore


def index(request):
    context = {'SHOPIFY_API_SCOPE': settings.SHOPIFY_API_SCOPE, 'request': RequestContext(request)}
    return render(request, 'shopify_app/index.html', context)


@never_cache
@transaction.atomic
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


@never_cache
@transaction.atomic
def facebook_campaign(request):
    context = {}
    if request.method == 'POST':
        campaign_type = request.GET.get('type')
        json_data = json.loads(request.body.decode('utf-8'))
        data = json_data.get('data')
        domain = json_data.get('shop')
        shop = ShopifyStore.objects.get(myshopify_domain=domain)
        facebook = FacebookBusinessManager.objects.get(myshopify_domain=domain)
        if shop and facebook:
            try:
                campaign = facebook.facebookcampaign_set.get(campaign_type=campaign_type)
            except FacebookCampaign.DoesNotExist:
                campaign = FacebookCampaign(business=facebook, campaign_type=campaign_type)
                campaign.save()
                campaign.facebookfeed_set.create(business=facebook)
                campaign.save()
            campaign.data = data
            campaign.save()
            fb_create_update(campaign.pk)
            _query = {
                'shop': domain, 'type': campaign_type
            }
            if not campaign.paid:
                context['url'] = route_url('shopify_app:fb_subscribe', _query=_query)

    return JsonResponse(context)


class BaseShop(object):

    def get_shop(self, domain):
        try:
            return ShopifyStore.objects.get(myshopify_domain=domain)
        except ShopifyStore.DoesNotExist:
            return None


class BaseFacebook(object):

    def get_facebook(self, domain):
        try:
            return FacebookBusinessManager.objects.get(myshopify_domain=domain)
        except FacebookBusinessManager.DoesNotExist:
            return None


class Dashboard(TemplateView, BaseShop, BaseFacebook):
    template_name = "shopify_app/dashboard.html"

    @property
    def feeds(self):
        feeds = {
            'fb': {
                'page_name': 'Your Facebook (Instagram) Feed',
                'title': "Facebook (Instagram) product feed set up!",
                'description': "Your have successfully generated your product feed. You can now add it to your Facebook Catalog.",
                'sectioned_title': "Your Facebook (Instagram) Feed",
                'link': 'facebook',
                'offer_count': 0,
                "catalog_title": "Facebook (Instagram) Catalog",
                "catalog_link": 'https://facebook.com/products/'
            },
            'ga': {
                'page_name': 'Your Google Feed',
                'title': "Google product feed set up!",
                'description': "Your have successfully generated your product feed. You can now add it to your Google Catalog.",
                'sectioned_title': "Your Google Feed",
                'link': 'google',
                'offer_count': 0,
                "catalog_title": "Google Merchants",
                "catalog_link": 'https://merchants.google.com/'
            },
            'yt': {
                'page_name': 'Your Yottos Feed',
                'title': "Yottos product feed set up!",
                'description': "Your have successfully generated your product feed. You can now add it to your Yottos Catalog.",
                'sectioned_title': "Your Yottos Feed",
                'link': 'yottos',
                'offer_count': 0,
                "catalog_title": "Yottos Adload",
                "catalog_link": 'https://adload.yottos.com/'
            },
            'pi': {
                'page_name': 'Your Pinterest Feed',
                'title': "Pinterest product feed set up!",
                'description': "Your have successfully generated your product feed. You can now add it to your Pinterest Catalog.",
                'sectioned_title': "Your Pinterest Feed",
                'link': 'pinterest',
                'offer_count': 0,
                "catalog_title": "Pinterest Catalog",
                "catalog_link": 'https://pinterest.com/product-catalogs/'
            },
        }
        if settings.FACEBOOK_APP_ENABLE:
            feeds['fb']['integration'] = {
                'complite': False,
                'data': {
                    'new_auditory': {
                        'geo': ["US"],
                        'budget': 15.00,
                        'status': False
                    },
                    'relevant': {
                        'geo': ["US"],
                        'budget': 15.00,
                        'status': False
                    },
                    'retargeting': {
                        'geo': ["US"],
                        'budget': 15.00,
                        'status': False
                    }
                },
                'text': {
                    'title': 'Automatically set up ad campaigns',
                    'description': 'Automatically setting up ad campaigns saves you time',
                    'sectioned_title': 'Activate automatic setup of advertising campaigns?',
                    'buttons': {
                        'activate': 'Activate automatic setup of advertising campaigns?',
                        'new_auditory': 'Create a new audience',
                        'relevant': 'Create Relevant Audiences',
                        'retargeting': 'Create retargeting'
                    },
                    'sheet': {
                        'new_auditory': {
                            'heading': 'New Audience Settings',
                            'cancel': 'Cancel',
                            'save': 'Create'
                        },
                        'relevant': {
                            'heading': 'Relevant Audience Settings',
                            'cancel': 'Cancel',
                            'save': 'Create'
                        },
                        'retargeting': {
                            'heading': 'Audience retargeting settings',
                            'cancel': 'Cancel',
                            'save': 'Create'
                        }
                    }
                }
            }

        return feeds

    @property
    def utm(self):
        return [
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

    @never_cache
    @transaction.atomic
    def get(self, request, *args, **kwargs):
        utm = []
        collection = []
        feed_name = kwargs.get('feed', 'fb')
        premium = False
        install = False
        reinstall = False
        storage = get_messages(request)
        for message in storage:
            if message.message == 'premium_active':
                premium = True
            elif message.message == 'install':
                install = True
            elif message.message == 'reinstall':
                reinstall = True
        feed = self.feeds.get(feed_name, self.feeds.get('fb'))
        shop = self.get_shop(request.shop)
        facebook = self.get_facebook(request.shop)
        if shop:
            feed_option = shop.feeds.get(feed_name, shop.feeds.get('fb'))
            collection = feed_option.get('collection', [])
            for item in self.utm:
                utm_val = feed_option.get('utm', {}).get(item.get('name'))
                if utm_val:
                    item['value'] = utm_val
                utm.append(item)

        if facebook and feed_name == 'fb' and feed.get('integration') is not None:
            feed['integration']['complite'] = facebook.connect
            for camp in facebook.facebookcampaign_set.all():
                if camp.campaign_type == 'new':
                    feed['integration']['text']['buttons']['new_auditory'] = 'Change New Audience Settings'
                    feed['integration']['data']['new_auditory']['geo'] = camp.data.get('geo', ["US"])
                    feed['integration']['data']['new_auditory']['budget'] = camp.data.get('budget', 100)
                    feed['integration']['data']['new_auditory']['status'] = camp.data.get('status', False)
                elif camp.campaign_type == 'rel':
                    feed['integration']['text']['buttons']['relevant'] = 'Change Relevant Audience Settings'
                    feed['integration']['data']['relevant']['geo'] = camp.data.get('geo', ["US"])
                    feed['integration']['data']['relevant']['budget'] = camp.data.get('budget', 100)
                    feed['integration']['data']['relevant']['status'] = camp.data.get('status', False)
                elif camp.campaign_type == 'ret':
                    feed['integration']['text']['buttons']['retargeting'] = 'Change Audience retargeting settings'
                    feed['integration']['data']['retargeting']['geo'] = camp.data.get('geo', ["US"])
                    feed['integration']['data']['retargeting']['budget'] = camp.data.get('budget', 100)
                    feed['integration']['data']['retargeting']['status'] = camp.data.get('status', False)

        context = {
            'page_name': feed['page_name'],
            'premium': premium,
            'install': install,
            'reinstall': reinstall,
            'shop': shop,
            'feed': feed,
            'utm': utm,
            'collection': collection,
            'feed_name': feed_name
        }
        return self.render_to_response(context)


class Downgrade(TemplateView, BaseShop):
    template_name = "shopify_app/downgrade.html"

    @never_cache
    def get(self, request, *args, **kwargs):
        shop = self.get_shop(request.shop)
        context = {
            'page_name': 'Downgrade to free Membership',
            'shop': shop,
        }

        return self.render_to_response(context)


class FbIntegration(TemplateView, BaseShop, BaseFacebook):
    template_name = "shopify_app/fb_integration.html"

    @never_cache
    def get(self, request, *args, **kwargs):
        shop = self.get_shop(request.shop)
        context = {
            'page_name': 'Connect Facebook',
            'shop': shop,
        }

        return self.render_to_response(context)

    @never_cache
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        json_data = json.loads(request.body.decode('utf-8'))
        data = json_data.get('data')
        domain = json_data.get('shop')
        user = json_data.get('user')
        token = json_data.get('token')
        shop = self.get_shop(domain=domain)
        facebook = self.get_facebook(domain=domain)
        business_id = data.get('business_id')
        account_id = data.get('account_id')
        page = data.get('page')
        pixel = data.get('pixel')
        if shop and business_id and account_id and pixel and user and token and page:
            if facebook is None:
                facebook = FacebookBusinessManager()
                facebook.myshopify_domain = domain
                facebook.access_token = token
            try:
                facebook.setup_access_token(token)
                facebook.user_id = user
                facebook.business_id = business_id
                facebook.account_id = account_id
                facebook.pixel = pixel
                facebook.page = page
                facebook.connect = True
                facebook.save()
            except Exception as e:
                print(e)
        return HttpResponse("OK")


class FbDisconect(TemplateView, BaseShop, BaseFacebook):
    template_name = "shopify_app/subscribe.html"

    @never_cache
    @transaction.atomic
    def get(self, request, *args, **kwargs):
        shop = self.get_shop(request.shop)
        facebook = self.get_facebook(request.shop)
        _query = {
            'shop': request.shop, 'hmac': request.hmac, 'timestamp': request.timestamp,
            'rand': int(datetime.timestamp(datetime.now()))
        }
        url = route_url('shopify_app:dashboard', _query=_query)
        if shop and facebook:
            facebook.delete()
        return self.render_to_response({'url': url})


class FbDeIntegration(TemplateView, BaseShop, BaseFacebook):
    template_name = "shopify_app/webhook.html"

    @never_cache
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        json_data = json.loads(request.body.decode('utf-8'))
        print(json_data)
        return self.render_to_response({})


class FbSubscribe(TemplateView, BaseShop, BaseFacebook):
    template_name = "shopify_app/subscribe.html"

    @never_cache
    @transaction.atomic
    def get(self, request, *args, **kwargs):
        campaign_type = request.GET.get('type')
        _query = {
            'shop': request.shop, 'hmac': request.hmac, 'timestamp': request.timestamp, 'type': campaign_type,
            'rand': int(datetime.timestamp(datetime.now()))
        }
        context = {'url': route_url('shopify_app:authenticate', _query=_query)}
        try:
            shop = self.get_shop(request.shop)
            facebook = self.get_facebook(request.shop)
            if shop and facebook:
                with shopify.Session.temp(shop.myshopify_domain, settings.SHOPIFY_API_VERSION, shop.access_token):
                    ac = shopify.ApplicationCharge()
                    if settings.SHOPIFY_TEST_PAY:
                        ac.test = True
                    ac.return_url = request.build_absolute_uri(
                        route_url('shopify_app:fb_subscribe_submit', _query=_query))
                    ac.price = 99.00
                    ac.name = "Setup Facebook campaign"
                    if ac.save():
                        context['url'] = ac.confirmation_url

        except Exception as e:
            print(e)
        return self.render_to_response(context)


class FbSubmitSubscribe(View, BaseShop, BaseFacebook):

    @never_cache
    @transaction.atomic
    def get(self, request, *args, **kwargs):
        campaign_type = request.GET.get('type')
        _query = {
            'shop': request.shop, 'hmac': request.hmac, 'timestamp': request.timestamp, 'type': campaign_type,
            'rand': int(datetime.timestamp(datetime.now()))
        }
        charge_id = request.GET.get('charge_id')
        shop = self.get_shop(request.shop)
        facebook = self.get_facebook(request.shop)
        if shop and facebook and charge_id:
            with shopify.Session.temp(shop.myshopify_domain, settings.SHOPIFY_API_VERSION, shop.access_token):
                ac = shopify.ApplicationCharge.find(charge_id)
                ac.activate()
                for campaign in facebook.facebookcampaign_set.all():
                    if campaign.campaign_type == campaign_type:
                        campaign.paid = True
                        campaign.save()
                        fb_create_update(campaign.pk)
        url = request.build_absolute_uri(route_url('shopify_app:dashboard_feeds', args=['fb'], _query=_query))
        return redirect(url)


class Authenticate(View, BaseShop):

    @never_cache
    def get(self, request, *args, **kwargs):
        shop = self.get_shop(request.shop)
        _query = {
            'shop': request.shop, 'hmac': request.hmac, 'timestamp': request.timestamp,
            'rand': int(datetime.timestamp(datetime.now()))
        }
        url = route_url('shopify_app:install', _query=_query)
        if shop and shop.installed:
            # _query['shop'] = shop.myshopify_domain
            url = route_url('shopify_app:dashboard', _query=_query)
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

    @never_cache
    def post(self, request, *args, **kwargs):
        shop = request.GET.get('shop') or request.POST.get('shop')
        _query = {
            'shop': re.sub(r'.*://?([^/?]+).*', '\g<1>', shop),
            'rand': int(datetime.timestamp(datetime.now()))
        }
        url = route_url('shopify_app:authenticate', _query=_query)
        return redirect(url)


class Install(View):

    @never_cache
    def get(self, request, *args, **kwargs):
        shop = request.shop
        _query = {
            'shop': request.shop, 'hmac': request.hmac, 'timestamp': request.timestamp,
            'rand': int(datetime.timestamp(datetime.now()))
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

    def create_shopify_store(self, shop_url, token, request):
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
                add_message(request, INFO, 'install')
            else:
                if obj.access_token != token:
                    obj.access_token = token
                    obj.installed = True
                    obj.feeds = feeds
                    obj.save()
                    add_message(request, INFO, 'reinstall')
                if not obj.installed:
                    obj.installed = True
                    obj.feeds = feeds
                    obj.save()
                    add_message(request, INFO, 'reinstall')

    def webhook_create(self, request, shop_url, token):
        with shopify.Session.temp(shop_url, settings.SHOPIFY_API_VERSION, token):
            webhook_data = {
                "topic": 'app/uninstalled',
                "address": request.build_absolute_uri(route_url('shopify_app:app_uninstalled')),
                "format": "json"
            }
            webhook = shopify.Webhook()
            w = webhook.create(webhook_data)

    @never_cache
    def get(self, request, *args, **kwargs):
        shop = request.shop
        _query = {
            'shop': request.shop, 'hmac': request.hmac, 'timestamp': request.timestamp,
            'rand': int(datetime.timestamp(datetime.now()))
        }
        url = route_url('shopify_app:dashboard', _query=_query)
        try:
            shopify_session = shopify.Session(shop, settings.SHOPIFY_API_VERSION)
            access_token = shopify_session.request_token(request.GET)
            self.create_shopify_store(shop, access_token, request)
            self.webhook_create(request, shop, access_token)
        except Exception:
            url = route_url('shopify_app:authenticate', _query=_query)
        return redirect(url)


class Subscribe(TemplateView, BaseShop):
    template_name = "shopify_app/subscribe.html"

    @never_cache
    def get(self, request, *args, **kwargs):
        _query = {
            'shop': request.shop, 'hmac': request.hmac, 'timestamp': request.timestamp,
            'rand': int(datetime.timestamp(datetime.now()))
        }
        context = {'url': route_url('shopify_app:authenticate', _query=_query)}
        try:
            shop = self.get_shop(request.shop)
            if shop:
                with shopify.Session.temp(shop.myshopify_domain, settings.SHOPIFY_API_VERSION, shop.access_token):
                    rac_count = 0
                    for i in shopify.RecurringApplicationCharge.find():
                        if i.status != 'declined':
                            rac_count += 1
                    rac = shopify.RecurringApplicationCharge()
                    if settings.SHOPIFY_TEST_PAY:
                        rac.test = True
                    rac.return_url = request.build_absolute_uri(
                        route_url('shopify_app:subscribe_submit', _query=_query))
                    rac.price = 29.00
                    if rac_count == 0:
                        rac.trial_days = 60
                        rac.trial_ends_on = (timezone.now() + timezone.timedelta(days=60)).isoformat()
                    rac.name = "Premium"
                    if rac.save():
                        context['url'] = rac.confirmation_url

        except Exception as e:
            print(e)
        return self.render_to_response(context)


class UnSubscribe(TemplateView, BaseShop):

    @never_cache
    @transaction.atomic
    def get(self, request, *args, **kwargs):
        _query = {
            'shop': request.shop, 'hmac': request.hmac, 'timestamp': request.timestamp,
            'rand': int(datetime.timestamp(datetime.now()))
        }
        shop = self.get_shop(request.shop)
        if shop:
            with shopify.Session.temp(shop.myshopify_domain, settings.SHOPIFY_API_VERSION, shop.access_token):
                rac = shopify.RecurringApplicationCharge.current()
                if rac:
                    rac.destroy()
                shop.premium = False
                shop.save()
        url = request.build_absolute_uri(route_url('shopify_app:dashboard', _query=_query))
        return redirect(url)


class SubmitSubscribe(View, BaseShop):

    @never_cache
    @transaction.atomic
    def get(self, request, *args, **kwargs):
        _query = {
            'shop': request.shop, 'hmac': request.hmac, 'timestamp': request.timestamp,
            'rand': int(datetime.timestamp(datetime.now()))
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
class WebhookAppUninstalled(TemplateView, BaseShop, BaseFacebook):
    template_name = "shopify_app/webhook.html"

    @never_cache
    def post(self, request, *args, **kwargs):
        if request.method == 'POST' and verify_webhook(request.body, request.headers.get('X-Shopify-Hmac-Sha256')):
            topic = request.headers.get('X-Shopify-Topic')
            shop_url = request.headers.get('X-Shopify-Shop-Domain')
            data = json.loads(request.body.decode('utf-8'))
            if topic == 'app/uninstalled':
                shop = self.get_shop(shop_url)
                facebook = self.get_facebook(shop_url)
                print('WebhookAppUninstalled', shop)
                if shop and facebook:
                    facebook.delete()
                if shop:
                    shop.installed = False
                    shop.premium = False
                    shop.date_uninstalled = timezone.now()
                    shop.save()

        return self.render_to_response({})


@method_decorator(csrf_exempt, name='dispatch')
class WebhookGDPR(TemplateView, BaseShop):
    template_name = "shopify_app/webhook.html"

    @never_cache
    def post(self, request, *args, **kwargs):
        return self.render_to_response({})


class MainXml(TemplateResponseMixin, View, BaseShop):
    template_name = "shopify_app/liquid/main.liquid"
    content_type = 'application/liquid'
    feed = None

    @never_cache
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
        context['utm'] = ''
        context['collections'] = ['collections.all.products']
        feed_settings = shop.feeds.get(self.feed, {})
        template = self.get_template_names()
        if shop is None:
            template = ["liquid/main.liquid"]
        else:
            def char_replace(string, chars=None, to_char=None):
                if chars is None:
                    chars = [' ', '.', ',', ';', '!', '?', ':', '<', '>', '&']
                if to_char is None:
                    to_char = '_'
                for ch in chars:
                    if ch in string:
                        string = string.replace(ch, to_char)
                return string.lower()

            cs = feed_settings.get('utm', {}).get('cs', self.feed)
            cn = feed_settings.get('utm', {}).get('cn', shop.myshopify_domain)
            cm = feed_settings.get('utm', {}).get('cm', 'cpc')
            utm = 'utm_source=%s&utm_medium=%s&utm_campaign=%s' % (
                char_replace(cs), char_replace(cm), char_replace(cn))
            collec = []
            for collection in feed_settings.get('collection', ''):
                if collection.get('value', False):
                    name = collection.get('name', 'yt__all')
                    if name != 'yt__all':
                        collec.append('collections.%s.products' % collection.get('name', 'all'))
                    else:
                        collec.append('collections.all.products')
            if len(collec) == 0:
                collec.append('collections.all.products')
            context['utm'] = utm
            context['collections'] = collec
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
    template_name = "shopify_app/liquid/ga_feed.liquid"
    feed = 'ga'


class FacebookXml(MainXml):
    template_name = "shopify_app/liquid/fb_feed.liquid"
    feed = 'fb'


class YottosXml(MainXml):
    template_name = "shopify_app/liquid/yt_feed.liquid"
    feed = 'yt'


class PinterestXml(MainXml):
    template_name = "shopify_app/liquid/pi_feed.liquid"
    feed = 'pi'
