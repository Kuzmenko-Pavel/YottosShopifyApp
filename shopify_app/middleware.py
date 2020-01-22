import re
import shopify
from django.conf import settings


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


class StripWhitespaceMiddleware(object):
    """
    Strips leading and trailing whitespace from response content.
    """

    def __init__(self, get_response=None):
        self.get_response = get_response
        self.whitespace = re.compile('^\s*\n', re.MULTILINE)
        self.whitespace_lead = re.compile('^\s+', re.MULTILINE)
        self.whitespace_trail = re.compile('\s+$', re.MULTILINE)
        self.new_line = re.compile('^\n*$', re.MULTILINE)

    def __call__(self, request):
        response = self.get_response(request)
        if "liquid" in response['Content-Type']:
            if hasattr(self, 'whitespace_lead'):
                response.content = self.whitespace_lead.sub('', response.content.decode('utf-8'))
            if hasattr(self, 'whitespace_trail'):
                response.content = self.whitespace_trail.sub('', response.content.decode('utf-8'))
            # Uncomment the next line to remove empty lines
            if hasattr(self, 'whitespace'):
                response.content = self.whitespace.sub('', response.content.decode('utf-8'))
            if hasattr(self, 'new_line'):
                response.content = self.new_line.sub('', response.content.decode('utf-8'))
            return response
        else:
            return response