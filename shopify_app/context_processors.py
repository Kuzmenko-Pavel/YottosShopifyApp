import shopify
from django.conf import settings
from .models import ShopifyStore


def current_shop(request):
    shop = request.GET.get('shop')
    print({'current_shop': shop, 'api_key': settings.SHOPIFY_API_KEY})
    return {'current_shop': shop, 'api_key': settings.SHOPIFY_API_KEY}
