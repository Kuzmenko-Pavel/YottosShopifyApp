from django.db import models
from django.db.models.fields import PositiveIntegerField
from django_mysql.models import Model


class PositiveBigIntegerField(PositiveIntegerField):
    """Represents MySQL's unsigned BIGINT data type (works with MySQL only!)"""
    empty_strings_allowed = False

    def get_internal_type(self):
        return "PositiveBigIntegerField"

    def db_type(self, connection):
        # This is how MySQL defines 64 bit unsigned integer data types
        return "bigint UNSIGNED"


class FacebookBusinessManager(Model):
    user_id = PositiveBigIntegerField()
    business_id = PositiveBigIntegerField()
    account_id = PositiveBigIntegerField()


class FacebookCampaign(Model):
    business = models.ForeignKey(FacebookBusinessManager, on_delete=models.CASCADE)
    campaign_id = PositiveBigIntegerField()


class FacebookFeed(Model):
    business = models.ForeignKey(FacebookBusinessManager, on_delete=models.CASCADE)
    campaign = models.ManyToManyField(FacebookCampaign)
    feed_id = PositiveBigIntegerField()
