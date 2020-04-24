from datetime import datetime, timedelta

import requests
from django.conf import settings
from django.db import models
from django.db.models.fields import BigIntegerField
from django_mysql.models import Model
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.business import Business
from facebook_business.adobjects.campaign import Campaign
from facebook_business.adobjects.productcatalog import ProductCatalog
from facebook_business.api import FacebookAdsApi


class FacebookBusinessManager(Model):
    myshopify_domain = models.CharField(max_length=100, help_text='Shopify store domain.', unique=True)
    user_id = BigIntegerField(null=True, blank=True)
    business_id = BigIntegerField(null=True, blank=True)
    account_id = BigIntegerField(null=True, blank=True)
    pixel = BigIntegerField(null=True, blank=True)
    page = BigIntegerField(null=True, blank=True)
    connect = models.BooleanField(help_text='App facebook connect.', default=False)
    access_token = models.TextField(help_text='Permanent token received from facebook.')
    access_token_end_date = models.DateTimeField(null=True, blank=True)

    def setup_access_token(self, token):
        r = requests.get('https://graph.facebook.com/%s/oauth/access_token?grant_type=fb_exchange_token&client_id=%s'
                         '&client_secret=%s&fb_exchange_token=%s' % ('v6.0', settings.FACEBOOK_APP_ID,
                                                                     settings.FACEBOOK_APP_SECRET, token
                                                                     ))
        rd = r.json()
        self.access_token = rd.get('access_token')
        self.access_token_end_date = datetime.now() + timedelta(seconds=rd.get('expires_in', 60 * 60 * 24 * 90))

    def setup_api_access(self):
        FacebookAdsApi.init(
            app_id=settings.FACEBOOK_APP_ID,
            app_secret=settings.FACEBOOK_APP_SECRET,
            access_token=self.access_token
        )


class FacebookCampaign(Model):
    CAMPAIGN_TYPE = (
        ('new', 'New Audience'),
        ('rel', 'Relevant Audience'),
        ('ret', 'Retargeting Audience'),

    )

    business = models.ForeignKey(FacebookBusinessManager, on_delete=models.CASCADE)
    campaign_id = BigIntegerField(null=True, blank=True)
    adset_id = BigIntegerField(null=True, blank=True)
    paid = models.BooleanField(default=False)
    campaign_type = models.CharField(
        max_length=3,
        choices=CAMPAIGN_TYPE,
        default=CAMPAIGN_TYPE[0],
    )

    def fb_get_or_create(self, domain):
        self.business.setup_api_access()

        for feed in self.facebookfeed_set.all():
            feed.fb_get_or_create(domain)

        name = 'Campaign %s %s (%s)' % (self.business.myshopify_domain, self.get_campaign_type_display(), self.id)
        campaign_params = {
            'name': name,
            'objective': Campaign.Objective.conversions,
            'special_ad_category': Campaign.SpecialAdCategory.none,
            'status': Campaign.Status.paused,
            'can_use_spend_cap': True,
            'can_create_brand_lift_study': False,
            'buying_type': "AUCTION",
            "budget_remaining": "0",
            "budget_rebalance_flag": False,
        }
        if self.paid:
            acc = AdAccount('act_%s' % self.business.account_id)
            if self.campaign_id:
                pass
            else:
                if acc:
                    campaign_result = acc.create_campaign(params=campaign_params)
                    self.campaign_id = campaign_result['id']

    def fb_get_or_create_adset(self):
        self.business.setup_api_access()
        if self.campaign_id:
            pass

class FacebookFeed(Model):
    business = models.ForeignKey(FacebookBusinessManager, on_delete=models.CASCADE)
    campaign = models.ForeignKey(FacebookCampaign, on_delete=models.CASCADE, default=None)
    feed_id = BigIntegerField(null=True, blank=True)
    catalog_id = BigIntegerField(null=True, blank=True)
    product_set_id = BigIntegerField(null=True, blank=True)

    def fb_get_or_create(self, domain):
        try:
            self.business.setup_api_access()
            try:
                catalog_params = {
                    'name': 'Catalog %s %s (%s)' % (self.business.myshopify_domain,
                                                    self.campaign.get_campaign_type_display(),
                                                    self.id),
                }

                acc = Business(self.business.business_id)
                if self.catalog_id:
                    pass
                else:
                    catalog = acc.create_owned_product_catalog(
                        params=catalog_params
                    )
                    catalog.add_external_event_sources(pixel_ids=[self.business.pixel, ])
                    self.catalog_id = catalog['id']
            except Exception as e:
                print(e)

            self.fb_feed_get_or_create()
            self.fb_product_set_get_or_create()
        except Exception as e:
            print(e)

    def fb_feed_get_or_create(self):
        try:
            self.business.setup_api_access()
            feed_url = 'https://%s/%s.xml' % (self.business.myshopify_domain, 'a/ytt_feed/facebook.xml')
            feed_url = 'https://cdn.yottos.com/sf.xml'
            feed_params = {
                'name': 'Feed %s %s (%s)' % (self.business.myshopify_domain,
                                             self.campaign.get_campaign_type_display(),
                                             self.id),
                'schedule': {'interval': 'DAILY',
                             'url': feed_url,
                             'hour': '22'},
            }
            if self.catalog_id:
                catalog = ProductCatalog(self.catalog_id)
                if catalog:
                    if self.feed_id:
                        pass
                    else:
                        feed = catalog.create_product_feed(params=feed_params)
                        self.feed_id = feed['id']
                        feed.create_upload(params={'url': feed_url})
        except Exception as e:
            print(e)

    def fb_product_set_get_or_create(self):
        try:
            self.business.setup_api_access()
            product_set_params = {'name': 'All lots %s %s (%s)' % (self.business.myshopify_domain,
                                                                   self.campaign.get_campaign_type_display(),
                                                                   self.id),
                                  'filter': {}}
            if self.catalog_id:
                catalog = ProductCatalog(self.catalog_id)
                if catalog:
                    if self.product_set_id:
                        pass
                    else:
                        product_set = catalog.create_product_set(params=product_set_params)
                        self.product_set_id = product_set['id']
        except Exception as e:
            print(e)
