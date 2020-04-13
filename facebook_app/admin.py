from django.contrib import admin

from .models import FacebookBusinessManager, FacebookCampaign, FacebookFeed

admin.site.register(FacebookBusinessManager)
admin.site.register(FacebookCampaign)
admin.site.register(FacebookFeed)
