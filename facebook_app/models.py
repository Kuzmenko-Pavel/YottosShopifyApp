from datetime import datetime, timedelta

import requests
from django.conf import settings
from django.db import models
from django.db.models.fields import BigIntegerField
from django_mysql.models import Model
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.campaign import Campaign
from facebook_business.api import FacebookAdsApi


class FacebookBusinessManager(Model):
    myshopify_domain = models.CharField(max_length=100, help_text='Shopify store domain.', unique=True)
    user_id = BigIntegerField()
    business_id = BigIntegerField()
    account_id = BigIntegerField()
    pixel = BigIntegerField()
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


class FacebookCampaign(Model):
    CAMPAIGN_TYPE = (
        ('new', 'New Audience'),
        ('rel', 'Relevant Audience'),
        ('ret', 'Retargeting Audience'),

    )

    business = models.ForeignKey(FacebookBusinessManager, on_delete=models.CASCADE)
    campaign_id = BigIntegerField(null=True, blank=True)
    paid = models.BooleanField(default=False)
    campaign_type = models.CharField(
        max_length=3,
        choices=CAMPAIGN_TYPE,
        default=CAMPAIGN_TYPE[0],
    )

    def fb_get_or_create(self):
        access_token = self.business.access_token
        FacebookAdsApi.init(
            app_id=settings.FACEBOOK_APP_ID,
            app_secret=settings.FACEBOOK_APP_SECRET,
            access_token=access_token
        )
        name = 'Campaign %s %s' % (self.business.myshopify_domain, self.get_campaign_type_display())
        params = {
            'name': name,
            'special_ad_category': Campaign.SpecialAdCategory.none,
            'objective': Campaign.Objective.conversions,
            'status': Campaign.Status.paused,
        }
        acc = AdAccount('act_%s' % self.business.account_id)
        if self.campaign_id:
            pass
        else:
            if acc:
                campaign_result = acc.create_campaign(params=params)
                self.campaign_id = campaign_result['id']


class FacebookFeed(Model):
    business = models.ForeignKey(FacebookBusinessManager, on_delete=models.CASCADE)
    campaign = models.ManyToManyField(FacebookCampaign)
    feed_id = BigIntegerField(null=True, blank=True)
