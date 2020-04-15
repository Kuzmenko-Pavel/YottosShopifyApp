import base64
import hashlib
import hmac
import json
from urllib.parse import urlencode

import shopify
from django.conf import settings
from django.shortcuts import reverse

from .models import ShopifyStore

SECRET = settings.SHOPIFY_API_SECRET
URL = settings.URL


def route_url(*args, **kwargs):
    query = kwargs.pop('_query', {})
    url = reverse(*args, **kwargs)
    if query:
        url += '?' + urlencode(query)
    return url


def verify_webhook(data, hmac_header):
    digest = hmac.new(SECRET.encode('utf-8'), data, hashlib.sha256).digest()
    computed_hmac = base64.b64encode(digest)

    return hmac.compare_digest(computed_hmac, hmac_header.encode('utf-8'))


class ShopifyHelper:
    def __init__(self, myshopify_domain):
        self._myshopify_domain = myshopify_domain
        try:
            self._user = ShopifyStore.objects.get(myshopify_domain=self._myshopify_domain)
        except Exception as e:
            raise e

        self._token, self._url = self._user.access_token, self._user.myshopify_domain

    def activate_session(self):
        shopify_session = shopify.Session(self._url, settings.SHOPIFY_API_VERSION, self._token)
        shopify.ShopifyResource.activate_session(shopify_session)

    def clear_session(self):
        shopify.ShopifyResource.clear_session()

    def get_user(self):
        return self._user

    def create_webhook(self):
        """Create webhook for listening events for inventory adjustment, product and variant deletion."""

        def address(name):
            return "https://" + settings.URL + reverse('shopify_app:' + name)

        try:
            webhooks = shopify.Webhook.find()
            if webhooks:
                print(webhooks)
                for _ in webhooks:
                    _.destroy()
            webhook = shopify.Webhook()
            for topic, link in [("inventory_levels/update", address('inventory_levels_update')),
                                ('inventory_items/update', address('inventory_items_update')),
                                ('products/update', address('products_update')),
                                ('inventory_items/delete', address('inventory_items_delete')),
                                ('products/delete', address('products_delete'))
                                ]:
                webhook_data = {
                    "topic": topic,
                    "address": link,
                    "format": "json"
                }
                print(webhook_data)
                w = webhook.create(webhook_data)
                for error in w.errors.errors:
                    print(error)
                print(shopify.Webhook.find())

        except Exception as e:
            print(e)


def parse_signed_request(signed_request, secret):
    l = signed_request.split('.', 2)
    encoded_sig = l[0]
    payload = l[1]

    sig = encoded_sig
    data = json.loads(payload)

    if data.get('algorithm').upper() != 'HMAC-SHA256':
        return None
    else:
        expected_sig = hmac.new(secret, msg=payload, digestmod=hashlib.sha256).digest()

    if sig != expected_sig:
        return None
    else:
        return data
