from django.db import models
from django.db.models.fields import BigIntegerField
from django_mysql.models import Model


class FacebookBusinessManager(Model):
    user_id = BigIntegerField()
    business_id = BigIntegerField()
    account_id = BigIntegerField()


class FacebookCampaign(Model):
    business = models.ForeignKey(FacebookBusinessManager, on_delete=models.CASCADE)
    campaign_id = BigIntegerField()


class FacebookFeed(Model):
    business = models.ForeignKey(FacebookBusinessManager, on_delete=models.CASCADE)
    campaign = models.ManyToManyField(FacebookCampaign)
    feed_id = BigIntegerField()
