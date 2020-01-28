from django.db import models
from django_mysql.models import JSONField, Model


def feeds_default():
    return {
        'fb': {
            'utm': {
                'cs': 'facebook',
                'cm': 'cpc',
                'cn': 'shop',
            },
            'collection': [
                {
                    'value': True,
                    'label': 'All Product',
                    'name': 'all',
                },
            ]
        },
        'ga': {
            'utm': {
                'cs': 'google',
                'cm': 'cpc',
                'cn': 'shop',
            },
            'collection': [
                {
                    'value': True,
                    'label': 'All Product',
                    'name': 'all',
                },
            ]
        },
        'yt': {
            'utm': {
                'cs': 'yottos',
                'cm': 'cpc',
                'cn': 'shop',
            },
            'collection': [
                {
                    'value': True,
                    'label': 'All Product',
                    'name': 'all',
                },
            ]
        },
        'pi': {
            'utm': {
                'cs': 'pinterest',
                'cm': 'cpc',
                'cn': 'shop',
            },
            'collection': [
                {
                    'value': True,
                    'label': 'All Product',
                    'name': 'all',
                },
            ]
        },
    }


class ShopifyStore(Model):
    """Model representing shopify stores which have installed this app."""
    name = models.CharField(max_length=100, help_text='Shopify store name.', null=True, blank=True)
    myshopify_domain = models.CharField(max_length=100, help_text='Shopify store domain.', unique=True)
    email = models.EmailField(max_length=100, help_text='Store email address.', null=True, blank=True)
    shop_owner = models.CharField(max_length=100, help_text='Shopify store owner name.', null=True, blank=True)
    country_name = models.CharField(max_length=100, help_text='Store location.', null=True, blank=True)
    access_token = models.CharField(max_length=100, help_text='Permanent token received from shopify.')
    installed = models.BooleanField(help_text='App installed.', default=False)
    date_installed = models.DateTimeField(help_text='App installation date.', null=True, blank=True)
    date_paid = models.DateTimeField(help_text='App paid date.', null=True, blank=True)
    date_uninstalled = models.DateTimeField(help_text='App uninstalled date.', null=True, blank=True)
    premium = models.BooleanField(help_text='App premium.', default=False)
    offer_count = models.IntegerField(help_text='Count offer.', default=0)
    feeds = JSONField(default=feeds_default)

    def __str__(self):
        """String representation for model object."""
        return self.name
