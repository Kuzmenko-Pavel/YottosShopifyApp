import datetime
import time

from django.http.response import HttpResponseBase
from django.utils import timezone
from django.utils.http import http_date


def my_set_cookie(self, key, value='', max_age=None, expires=None, path='/',
                  domain=None, secure=False, httponly=False, samesite=None):
    """
    Set a cookie.

    ``expires`` can be:
    - a string in the correct format,
    - a naive ``datetime.datetime`` object in UTC,
    - an aware ``datetime.datetime`` object in any time zone.
    If it is a ``datetime.datetime`` object then calculate ``max_age``.
    """
    self.cookies[key] = value
    if expires is not None:
        if isinstance(expires, datetime.datetime):
            if timezone.is_aware(expires):
                expires = timezone.make_naive(expires, timezone.utc)
            delta = expires - expires.utcnow()
            # Add one second so the date matches exactly (a fraction of
            # time gets lost between converting to a timedelta and
            # then the date string).
            delta = delta + datetime.timedelta(seconds=1)
            # Just set max_age - the max_age logic will set expires.
            expires = None
            max_age = max(0, delta.days * 86400 + delta.seconds)
        else:
            self.cookies[key]['expires'] = expires
    else:
        self.cookies[key]['expires'] = ''
    if max_age is not None:
        self.cookies[key]['max-age'] = max_age
        # IE requires expires, so set it if hasn't been already.
        if not expires:
            self.cookies[key]['expires'] = http_date(time.time() + max_age)
    if path is not None:
        self.cookies[key]['path'] = path
    if domain is not None:
        self.cookies[key]['domain'] = domain
    if secure:
        self.cookies[key]['secure'] = True
    if httponly:
        self.cookies[key]['httponly'] = True
    if samesite:
        if samesite.lower() not in ('lax', 'strict', 'none'):
            raise ValueError('samesite must be "lax" or "strict" or "none".')
        self.cookies[key]['samesite'] = samesite


HttpResponseBase.set_cookie = my_set_cookie
