from django.conf import settings


def current_shop(request):
    shop = request.GET.get('shop')
    return {'current_shop': shop, 'api_key': settings.SHOPIFY_API_KEY}
