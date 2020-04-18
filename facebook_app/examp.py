from facebook_business.adobjects.ad import Ad
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.adcreative import AdCreative
from facebook_business.adobjects.adcreativeobjectstoryspec import AdCreativeObjectStorySpec
from facebook_business.adobjects.adpromotedobject import AdPromotedObject
from facebook_business.adobjects.adset import AdSet
from facebook_business.adobjects.campaign import Campaign
from facebook_business.adobjects.flexibletargeting import FlexibleTargeting
from facebook_business.adobjects.targeting import Targeting
from facebook_business.api import FacebookAdsApi

access_token = 'EAAKUTF2LgQABAKf6CQudODVyykgAUsmYsixtbeylc0wmjRPhFHZCIjjZCZBWN06Dk2adBY8cLAcoY0QgeOrMu2AjQW5p6QsD2eB0nsLAF2xdDiMznlUNuXdbodGAEDutPZCS17YO810qhNgzI5j6XEgFL5vrx7erIUQp9vZA2KmsRiKJlk9AX'
FacebookAdsApi.init(
    app_id='253196639189259',
    app_secret='8a508d430429585246326686016c48db',
    access_token='EAADmRZBZB8uQsBAOd8vEFJCkWHOqFF2i2WcZAmby0uU3wNzTOjdHrGaX3qwe8ZAQrlb5ZBMsBef9ZBEvdh7ni2xbaCMxmVjmrUi315zEcnYuDZBlEbmdfoeTsjPRvCKT92fNeH4uk8nmes4ai9dsLg4zJRrcxKEZBS3ZCQD5QKYW2KQZDZD'
)
# FacebookAdsApi.init(
#     app_id='726005661270272',
#     app_secret='bc3c46925dc37a5a01549d791f81dc12',
#     access_token=access_token
#     )
business_id = '183065162237916'
account_id = '210542543578120'
# account_id = '869325563535981'
pixel = '217796929477510'
user = '623664381519741'
feed_id = '243910640095552'
catalog_id = '586708951936950'
product_set_id = '264939684662414'
page_id = '509042519132613'

acc = AdAccount('act_%s' % account_id)
print(acc)

campaign_params = {
    'name': 'Test New Campaign',
    'objective': Campaign.Objective.conversions,
    'special_ad_category': Campaign.SpecialAdCategory.none,
    'status': Campaign.Status.paused,
    'can_use_spend_cap': True,
    'can_create_brand_lift_study': False,
    'buying_type': "AUCTION",
    "budget_remaining": "0",
    "budget_rebalance_flag": False,
}
campaign = acc.create_campaign(params=campaign_params)
print(campaign)

adset_params = {
    'name': 'Test New  AdSet',
    'bid_strategy': AdSet.BidStrategy.lowest_cost_without_cap,
    'billing_event': AdSet.BillingEvent.impressions,
    "budget_remaining": "975",  # ?
    'campaign_id': campaign["id"],
    'status': AdSet.Status.paused,
    'daily_budget': 1600,
    "destination_type": AdSet.DestinationType.undefined,
    "is_dynamic_creative": False,
    "lifetime_budget": "0",
    "lifetime_imps": 0,
    'optimization_goal': AdSet.OptimizationGoal.offsite_conversions,
    'optimization_sub_event': AdSet.OptimizationSubEvent.none,
    'pacing_type': ["standard"],
    'promoted_object': {
        "custom_event_type": AdPromotedObject.CustomEventType.purchase,
        "pixel_id": pixel
    },
    "targeting": {
        Targeting.Field.age_max: 65,
        Targeting.Field.age_min: 22,
        Targeting.Field.flexible_spec: [
            {
                FlexibleTargeting.Field.interests: [
                    {
                        "id": "6011366104268",
                        "name": "Женская одежда"
                    },
                    {
                        "id": "6011994253127",
                        "name": "Мужская одежда"
                    }
                ]
            },
            {
                FlexibleTargeting.Field.interests: [
                    {
                        "id": "6003346592981",
                        "name": "Онлайн-покупки"
                    }
                ],
                FlexibleTargeting.Field.behaviors: [
                    {
                        "id": "6071631541183",
                        "name": "Вовлеченные покупатели"
                    }
                ]
            }
        ],
        Targeting.Field.geo_locations: {
            'countries': ['UA'],
            "location_types": [
                "home",
                "recent"
            ]
        },
        Targeting.Field.targeting_optimization: 'none',
        Targeting.Field.publisher_platforms: ["facebook", ],
        Targeting.Field.facebook_positions: ["feed", ],
        Targeting.Field.device_platforms: [Targeting.DevicePlatforms.mobile,
                                           Targeting.DevicePlatforms.desktop],
    }
}

adset = acc.create_ad_set(params=adset_params)
print(adset)

story = AdCreativeObjectStorySpec()
story[story.Field.page_id] = page_id
story[story.Field.template_data] = {
    "link": "http://yottos.com/",
    "name": "{{product.name}}",
    "description": "{{product.current_price strip_zeros}}",
    "call_to_action": {
        "type": "SHOP_NOW"
    },
    "multi_share_end_card": False,
    "show_multiple_images": False
}

params_ad_creative = {
    'name': 'Test New  Ad Template',
    AdCreative.Field.object_story_spec: story,
    AdCreative.Field.product_set_id: product_set_id,
    # AdCreative.Field.call_to_action_type: AdCreative.CallToActionType.shop_now,
    AdCreative.Field.object_type: AdCreative.ObjectType.share,
    AdCreative.Field.title: "{{product.name}}",
}
creative = None
try:
    creative = acc.create_ad_creative(params=params_ad_creative)
    print(creative)
except Exception as e:
    print(e._body)

params_ads = {
    Ad.Field.name: 'Test New  Ad',
    Ad.Field.adset_id: adset['id'],
    # Ad.Field.creative: {'creative_id': creative['id']},
    Ad.Field.status: 'PAUSED',
    # Ad.Field.name.tracking_specs: [
    #     {
    #         "action.type": [
    #             "offsite_conversion"
    #         ],
    #         "fb_pixel": [
    #             pixel
    #         ]
    #     },
    #     {
    #         "action.type": [
    #             "post_engagement"
    #         ],
    #         "page": [
    #             page_id
    #         ],
    #         "post": [
    #             "2827957023907806"
    #         ]
    #     },
    #     {
    #         "action.type": [
    #             "link_click"
    #         ],
    #         "post": [
    #             "2827957023907806"
    #         ],
    #         "post.wall": [
    #             page_id
    #         ]
    #     }
    # ]
}
if creative:
    params_ads[Ad.Field.creative] = {'creative_id': creative['id']}

ads = acc.create_ad(params=params_ads)
print(ads)
