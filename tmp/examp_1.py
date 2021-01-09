import json

from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.adset import AdSet
from facebook_business.adobjects.business import Business
from facebook_business.adobjects.campaign import Campaign
from facebook_business.adobjects.targeting import Targeting
from facebook_business.api import FacebookAdsApi

# # short_access_token = 'EAAKUTF2LgQABANoIlZCidhALkqyVADwyd3TKIVsDDMU1RHtOBmdynpFeeOxatBblM1zzgIZAFEN6FhLnRpZCFDOnU2DbaLkk2zL3pT3rJ3CMu6kjX7rv305tIRnZC1LA8pAu0MFnCJGZBO0mCORZCv1DhRhkeQZCygoZAA3N7fAcdB1CThhl9Iwbk6y4mkiIyD6CKFYuDuA0ClLTgZB98YDZAmaW4VqmhEfVbZAZAvNpQxoGjVA7wnTuPLspLwKBVz4ZA5GwZD'
# access_token = 'EAAKUTF2LgQABAN4dhpZAu5zNZAztm0glWYeeIVUXl8aLGjBx0ZAqJ1ZB6DsBZBUvL04mIutn9oh6kn4SRH7xgiED1ceZA5aDl3Nn8z4M32Ifmh3p4HYITtZCgLj4IJsvLZBfsiaIa6v9JtgDzGx5jdLZB02f563NyuBfEvRWiURS6Fe0szWapDunj'
# app_secret = 'bc3c46925dc37a5a01549d791f81dc12'
# app_id = '726005661270272'
#
# r = requests.get('https://graph.facebook.com/%s/oauth/access_token?grant_type=fb_exchange_token&client_id=%s'
#                  '&client_secret=%s&fb_exchange_token=%s' % ('v6.0', app_id, app_secret, access_token))
# rd = r.json()
# print(rd)
# new_access_token = rd.get('access_token')
# print(new_access_token == access_token)
#
# new_access_token = 'EAAKUTF2LgQABAC3nibo5lwj9KQyNxFZBKSRzDdLCJ31waewRrgm8ZBD9Y7gDaO7YrLCtpRIl1ZBWjcd7KLE1R1GURx7WwJlsx5eZCqMQbVnEEVdtYAiOKobTu9ifyBvNYF63UB1eLXRPGxSKX00GH7ZCL0YQO8wQAu16PTZAEdEmrC2FTNbPEnZCSlw1VSiA0ZC2cmHLVwE78gZDZD'
#
# FacebookAdsApi.init(access_token=new_access_token)
# me = User(fbid='me').api_get(
#     fields=[User.Field.email, User.Field.currency, User.Field.name, User.Field.timezone, User.Field.link])
# print(me)
# my_accounts = list(me.get_ad_accounts(fields=[AdAccount.Field.name]))
# print(my_accounts)
# my_business = list(me.get_businesses())
# print(my_business)
# catalog_params = {
#     'name': 'Test Catalog',
# }
# feed_url = 'https://cdn.yottos.com/sf.xml'
# feed_params = {
#     'name': 'Test Feed',
#     'schedule': {'interval': 'DAILY',
#                  'url': feed_url,
#                  'hour': '22'},
# }
# bic = Business(business_id)
# print(bic)
# catalog = bic.create_owned_product_catalog(
#     params=catalog_params
# )
# catalog.add_external_event_sources(pixel_ids=[pixel, ])
# print(catalog)
# feed = catalog.create_product_feed(params=feed_params)
# print(feed)
# print(feed.create_upload(params={'url': feed_url}))
# product_set = catalog.create_product_set(params={'name': 'All', 'filter': {}})
# print(product_set)
#
# campaign_params = {
#     'name': 'Test Campaign',
#     'special_ad_category': Campaign.SpecialAdCategory.none,
#     'objective': Campaign.Objective.conversions,
#     'status': Campaign.Status.paused,
# }
# acc = AdAccount('act_%s' % account_id)
# print(acc)
#
# campaign = acc.create_campaign(params=campaign_params)
# print(campaign)
#
# adset_params = {
#     'name': 'TEST ADSET',
#     'campaign_id': campaign["id"],
#     'daily_budget': 10000,
#     'bid_strategy': AdSet.BidStrategy.lowest_cost_with_bid_cap,
#     'billing_event': AdSet.BillingEvent.impressions,
#     'optimization_goal': AdSet.OptimizationGoal.offsite_conversions,
#     'bid_amount': 20,
#     'targeting': {
#         Targeting.Field.geo_locations: {
#             'countries': ['UA'],
#         },
#         Targeting.Field.device_platforms: [Targeting.DevicePlatforms.desktop, Targeting.DevicePlatforms.mobile],
#         'publisher_platforms': ['facebook'],
#         'promoted_object': {
#             'product_set_id': pixel,
#             "custom_event_type": "PURCHASE",
#         },
#         Targeting.Field.product_audience_specs: [
#                 {
#                     'product_set_id': product_set['id'],
#                     'inclusions': [
#                         {
#                             'retention_seconds': 86400,
#                             'rule': {
#                                 'event': {
#                                     'eq': 'ViewContent',
#                                 },
#                             },
#                         },
#                     ],
#                 },
#             ],
#     },
#     'promoted_object': {
#         'product_catalog_id': catalog['id'],
#     },
#     'status': AdSet.Status.paused
# }
# print(json.dumps(adset_params))
# adset = acc.create_ad_set(params=adset_params)
# print(adset)
FacebookAdsApi.init(
    app_id='253196639189259',
    app_secret='8a508d430429585246326686016c48db',
    access_token='EAADmRZBZB8uQsBAOd8vEFJCkWHOqFF2i2WcZAmby0uU3wNzTOjdHrGaX3qwe8ZAQrlb5ZBMsBef9ZBEvdh7ni2xbaCMxmVjmrUi315zEcnYuDZBlEbmdfoeTsjPRvCKT92fNeH4uk8nmes4ai9dsLg4zJRrcxKEZBS3ZCQD5QKYW2KQZDZD'
)
business_id = '183065162237916'
account_id = '210542543578120'
pixel = '217796929477510'
user = '623664381519741'



