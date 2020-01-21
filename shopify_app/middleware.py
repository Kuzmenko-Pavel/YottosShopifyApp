from django.conf import settings
import shopify


class ConfigurationError(BaseException):
    pass


class LoginProtection(object):
    def __init__(self, get_response=None):
        self.get_response = get_response
        self.api_key = settings.SHOPIFY_API_KEY
        self.api_secret = settings.SHOPIFY_API_SECRET
        if not self.api_key or not self.api_secret:
            raise ConfigurationError("SHOPIFY_API_KEY and SHOPIFY_API_SECRET must be set in ShopifyAppConfig")
        shopify.Session.setup(api_key=self.api_key, secret=self.api_secret)

    def __call__(self, request):
        request.shop = request.GET.get('shop', '')
        request.hmac = request.GET.get('hmac', '')
        request.timestamp = request.GET.get('timestamp', '')
        response = self.get_response(request)
        return response