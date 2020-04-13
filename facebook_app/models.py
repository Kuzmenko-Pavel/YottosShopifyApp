from datetime import datetime, timedelta

import requests
from django.db import models
from django.db.models.fields import BigIntegerField
from django_mysql.models import Model

app_secret = 'bc3c46925dc37a5a01549d791f81dc12'
app_id = '726005661270272'

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
                         '&client_secret=%s&fb_exchange_token=%s' % ('v6.0', app_id, app_secret, token))
        rd = r.json()
        self.access_token = rd.get('access_token')
        self.access_token_end_date = datetime.now() + timedelta(seconds=rd.get('expires_in'))


class FacebookCampaign(Model):
    CAMPAIGN_TYPE = (
        ('new', 'New Audience'),
        ('rel', 'Relevant Audience'),
        ('ret', 'Retargeting Audience'),

    )

    business = models.ForeignKey(FacebookBusinessManager, on_delete=models.CASCADE)
    campaign_id = BigIntegerField()
    campaign_type = models.CharField(
        max_length=3,
        choices=CAMPAIGN_TYPE,
        default=CAMPAIGN_TYPE[0],
    )


class FacebookFeed(Model):
    business = models.ForeignKey(FacebookBusinessManager, on_delete=models.CASCADE)
    campaign = models.ManyToManyField(FacebookCampaign)
    feed_id = BigIntegerField()
