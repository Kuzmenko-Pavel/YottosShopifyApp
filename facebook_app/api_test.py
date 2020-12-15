from time import sleep
from datetime import datetime
from pprint import pprint
import json

from facebook_business.adobjects.ad import Ad
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.adcreative import AdCreative
from facebook_business.adobjects.adcreativeobjectstoryspec import AdCreativeObjectStorySpec
from facebook_business.adobjects.adpromotedobject import AdPromotedObject
from facebook_business.adobjects.adset import AdSet
from facebook_business.adobjects.business import Business
from facebook_business.adobjects.campaign import Campaign
from facebook_business.adobjects.flexibletargeting import FlexibleTargeting
from facebook_business.adobjects.productcatalog import ProductCatalog
from facebook_business.adobjects.targeting import Targeting
from facebook_business.api import FacebookAdsApi
from facebook_business.exceptions import FacebookRequestError

FACEBOOK_APP_ID = '726005661270272'
FACEBOOK_APP_SECRET = 'bc3c46925dc37a5a01549d791f81dc12'
access_token = 'EAAKUTF2LgQABAMDDg1nZAEa0CqG8EFCGuUQalGojYs82yoQNo0xd9dZAaWkkrx40vNkbUmpnFuhYyynQ3xs7wN0EH41MMxx15bXgrYDyZAcA02V6C8slQYtRLmaIHyfwYn8y9Cik7cki4IYzhJdI3V2FO6ZBZArA7mZBZCTb7jaowZDZD'
business_id = '183065162237916'
account_id = '210542543578120'
pixel = '217796929477510'
page = '509042519132613'
trolling = False

data = {
    'new': {
        'catalog_id': None,
        'feed_id': None,
        'product_set_id': None,
        'campaign_id': None,
        'adset_id': None,
        'ad_creative_id': None,
        'ads_id': None
    },
    'rel': {
        'catalog_id': None,
        'feed_id': None,
        'product_set_id': None,
        'campaign_id': None,
        'adset_id': None,
        'ad_creative_id': None,
        'ads_id': None
    },
    'ret': {
        'catalog_id': None,
        'feed_id': None,
        'product_set_id': None,
        'campaign_id': None,
        'adset_id': None,
        'ad_creative_id': None,
        'ads_id': None
    },

}


def print_url(r, *args, **kwargs):
    global trolling
    if r.headers.get('x-business-use-case-usage'):
        usage = json.loads(r.headers.get('x-business-use-case-usage'))
        for k, v in usage.items():
            d = v[0]
            # pprint(d)
            sleep_sec = max(d['total_time'], d['call_count'], d['total_cputime'])
            if sleep_sec > 80 and not trolling:
                trolling = True
            elif sleep_sec < 45 and trolling:
                trolling = False

            if trolling:
                sleep(sleep_sec)


def setup_api_access():
    api = FacebookAdsApi.init(
        app_id=FACEBOOK_APP_ID,
        app_secret=FACEBOOK_APP_SECRET,
        access_token=access_token,
        debug=False
    )
    api._session.requests.hooks = {'response': print_url}


def get_params(campaign_type):
    camp_status = Campaign.Status.paused
    adset_status = AdSet.Status.paused
    budget = '5000'
    countries = ["US", ]

    story = AdCreativeObjectStorySpec()
    story[story.Field.page_id] = page
    story[story.Field.template_data] = {
        "link": "https://yottos.com/",
        "name": "{{product.name}}",
        "description": "{{product.current_price strip_zeros}}",
        "call_to_action": {
            "type": "SHOP_NOW"
        },
        "multi_share_end_card": False,
        "show_multiple_images": False
    }
    story_ret = AdCreativeObjectStorySpec()
    story_ret[story.Field.page_id] = page
    story_ret[story.Field.template_data] = {
        "link": "https://yottos.com/",
        "name": "{{product.name}}",
        "description": "{{product.description}} ",
        "call_to_action": {
            "type": "SHOP_NOW"
        },
        "multi_share_end_card": False,
        "show_multiple_images": False,
        "image_layer_specs": [
            {
                "image_source": "catalog",
                "layer_type": "image"
            },
            {
                "content": {
                    "type": "price"
                },
                "layer_type": "text_overlay",
                "opacity": 100,
                "overlay_position": "top_left",
                "overlay_shape": "rectangle",
                "shape_color": "DF0005",
                "text_color": "FFFFFF",
                "text_font": "open_sans_bold"
            }
        ]
    }

    params = {
        'new': {
            'campaign': {
                'name': 'Campaign new test api call',
                'objective': Campaign.Objective.conversions,
                'special_ad_category': Campaign.SpecialAdCategory.none,
                'status': camp_status,
                'can_use_spend_cap': True,
                'can_create_brand_lift_study': False,
                'buying_type': "AUCTION",
                "budget_remaining": "0",
                "budget_rebalance_flag": False,
            },
            'adset': {
                'name': 'AdSet new test api call',
                'bid_strategy': AdSet.BidStrategy.lowest_cost_without_cap,
                'billing_event': AdSet.BillingEvent.impressions,
                'campaign_id': data['new']['campaign_id'],
                'status': adset_status,
                'daily_budget': budget,
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
                        # {
                        #     FlexibleTargeting.Field.interests: [
                        #         {
                        #             "id": "6011366104268",
                        #             "name": "Женская одежда"
                        #         },
                        #         {
                        #             "id": "6011994253127",
                        #             "name": "Мужская одежда"
                        #         }
                        #     ]
                        # },
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
                        'countries': countries,
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

            },
            'ad_creative': {
                'name': 'Ad Template new test api call %s' % str(datetime.now().timestamp()),
                AdCreative.Field.object_story_spec: story,
                AdCreative.Field.product_set_id: data['new']['product_set_id'],
                # AdCreative.Field.call_to_action_type: AdCreative.CallToActionType.shop_now,
                AdCreative.Field.object_type: AdCreative.ObjectType.share,
                AdCreative.Field.title: "{{product.name}}",
            },
            'ads': {
                Ad.Field.name: 'Ad new test api call',
                Ad.Field.adset_id: data['new']['adset_id'],
                Ad.Field.creative: {'creative_id': data['new']['ad_creative_id']},
                Ad.Field.status: adset_status,
                Ad.Field.tracking_specs: {
                        "action.type": [
                            "offsite_conversion"
                        ],
                        "fb_pixel": [
                            pixel
                        ]
                    }
            }
        },
        'rel': {
            'campaign': {
                'name': 'Campaign rel test api call',
                'objective': Campaign.Objective.conversions,
                'special_ad_category': Campaign.SpecialAdCategory.none,
                'status': camp_status,
                'can_use_spend_cap': True,
                'can_create_brand_lift_study': False,
                'buying_type': "AUCTION",
                "budget_remaining": "0",
                "budget_rebalance_flag": False,
            },
            'adset': {
                'name': 'AdSet rel test api call',
                'bid_strategy': AdSet.BidStrategy.lowest_cost_without_cap,
                'billing_event': AdSet.BillingEvent.impressions,
                'campaign_id': data['rel']['campaign_id'],
                'status': adset_status,
                'daily_budget': budget,
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
                        # {
                        #     FlexibleTargeting.Field.interests: [
                        #         {
                        #             "id": "6011366104268",
                        #             "name": "Женская одежда"
                        #         },
                        #         {
                        #             "id": "6011994253127",
                        #             "name": "Мужская одежда"
                        #         }
                        #     ]
                        # },
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
                        'countries': countries,
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

            },
            'ad_creative': {
                'name': 'Ad Template rel test api call %s' % str(datetime.now().timestamp()),
                AdCreative.Field.object_story_spec: story,
                AdCreative.Field.product_set_id: data['rel']['product_set_id'],
                # AdCreative.Field.call_to_action_type: AdCreative.CallToActionType.shop_now,
                AdCreative.Field.object_type: AdCreative.ObjectType.share,
                AdCreative.Field.title: "{{product.name}}",
            },
            'ads': {
                Ad.Field.name: 'Ad rel test api call',
                Ad.Field.adset_id: data['rel']['adset_id'],
                Ad.Field.creative: {'creative_id': data['rel']['ad_creative_id']},
                Ad.Field.status: adset_status,
                Ad.Field.tracking_specs: [
                    {
                        "action.type": [
                            "offsite_conversion"
                        ],
                        "fb_pixel": [
                            pixel
                        ]
                    },
                    {
                        "action.type": [
                            "post_engagement"
                        ],
                        "page": [
                            page
                        ],
                        # "post": [
                        #     "2827957023907806"
                        # ]
                    },
                    {
                        "action.type": [
                            "link_click"
                        ],
                        # "post": [
                        #     "2827957023907806"
                        # ],
                        "post.wall": [
                            page
                        ]
                    }
                ]
            }
        },
        'ret': {
            'campaign': {
                'name': 'Campaign ret test api call',
                'objective': Campaign.Objective.product_catalog_sales,
                'special_ad_category': Campaign.SpecialAdCategory.none,
                'status': camp_status,
                'can_use_spend_cap': True,
                'can_create_brand_lift_study': False,
                'buying_type': "AUCTION",
                "budget_remaining": "0",
                "budget_rebalance_flag": False,
                'promoted_object': {
                    "product_catalog_id": data['ret']['catalog_id']
                },
            },
            'adset': {
                'name': 'AdSet ret test api call',
                'bid_strategy': AdSet.BidStrategy.lowest_cost_without_cap,
                'billing_event': AdSet.BillingEvent.impressions,
                'campaign_id': data['ret']['campaign_id'],
                'status': adset_status,
                'daily_budget': budget,
                "destination_type": AdSet.DestinationType.website,
                "is_dynamic_creative": False,
                "lifetime_budget": "0",
                "lifetime_imps": 0,
                'optimization_goal': AdSet.OptimizationGoal.offsite_conversions,
                'optimization_sub_event': AdSet.OptimizationSubEvent.none,
                'pacing_type': ["standard"],
                'promoted_object': {
                    "custom_event_type": AdPromotedObject.CustomEventType.purchase,
                    "product_set_id": data['ret']['product_set_id']
                },
                "targeting": {
                    Targeting.Field.age_max: 65,
                    Targeting.Field.age_min: 22,
                    Targeting.Field.product_audience_specs: [
                        {
                            "product_set_id": data['ret']['product_set_id'],
                            "inclusions": [
                                {
                                    "retention_seconds": "1209600",
                                    "rule": "{\"event\":{\"eq\":\"ViewContent\"}}"
                                },
                                {
                                    "retention_seconds": "1209600",
                                    "rule": "{\"event\":{\"eq\":\"AddToCart\"}}"
                                }
                            ],
                            "exclusions": [
                                {
                                    "retention_seconds": "1209600",
                                    "rule": "{\"event\":{\"eq\":\"Purchase\"}}"
                                }
                            ]
                        }
                    ],
                    Targeting.Field.geo_locations: {
                        'countries': countries,
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

            },
            'ad_creative': {
                'name': 'Ad Template ret test api call %s' % str(datetime.now().timestamp()),
                AdCreative.Field.object_story_spec: story_ret,
                AdCreative.Field.product_set_id: data['ret']['product_set_id'],
                # AdCreative.Field.call_to_action_type: AdCreative.CallToActionType.shop_now,
                AdCreative.Field.object_type: AdCreative.ObjectType.share,
                AdCreative.Field.title: "{{product.name}}",
            },
            'ads': {
                Ad.Field.name: 'Ad ret test api call',
                Ad.Field.adset_id: data['ret']['adset_id'],
                Ad.Field.creative: {'creative_id': data['ret']['ad_creative_id']},
                Ad.Field.status: adset_status,
                Ad.Field.tracking_specs: [
                    {
                        "action.type": [
                            "offsite_conversion"
                        ],
                        "fb_pixel": [
                            pixel
                        ]
                    },
                    {
                        "action.type": [
                            "post_engagement"
                        ],
                        "page": [
                            page
                        ],
                        # "post": [
                        #     "2827957023907806"
                        # ]
                    },
                    {
                        "action.type": [
                            "link_click"
                        ],
                        # "post": [
                        #     "2827957023907806"
                        # ],
                        "post.wall": [
                            page
                        ]
                    }
                ]
            }
        }
    }
    return params[campaign_type]


def create_catalog(campaign_type):
    setup_api_access()
    try:
        catalog_params = {
            'name': 'Catalog test %s api call' % campaign_type,
        }

        acc = Business(business_id)
        if data[campaign_type]['catalog_id']:
            print("Catalog existing '%s'" % data[campaign_type]['catalog_id'])
        else:
            print("Catalog not existing")
            catalog = acc.create_owned_product_catalog(
                params=catalog_params
            )
            catalog.add_external_event_sources(pixel_ids=[pixel, ])
            data[campaign_type]['catalog_id'] = catalog['id']
            print("Catalog creating '%s'" % data[campaign_type]['catalog_id'])
    except FacebookRequestError as e:
        print(e._body.get('error', {}).get('message'))
        # print(e)
    except Exception as e:
        # print(e)
        pass


def delete_catalog(campaign_type):
    setup_api_access()
    try:
        if data[campaign_type]['catalog_id']:
            catalog = ProductCatalog(data[campaign_type]['catalog_id'])
            if catalog:
                catalog.api_delete()
                data[campaign_type]['catalog_id'] = None
                data[campaign_type]['feed_id'] = None
                data[campaign_type]['product_set_id'] = None
                print("Catalog deleted '%s'" % data[campaign_type]['catalog_id'])
            else:
                print("Catalog not existing")
        else:
            print("Catalog not existing")
    except FacebookRequestError as e:
        print(e._body.get('error', {}).get('message'))
        # print(e)
    except Exception as e:
        # print(e)
        pass


def create_feed(campaign_type):
    setup_api_access()
    try:
        feed_url = 'https://cdn.yottos.com/sf.xml'
        feed_params = {
            'name': 'Feed test %s api call' % campaign_type,
            'schedule': json.dumps({'interval': 'DAILY', 'url': feed_url, 'hour': '22'}),
        }
        if data[campaign_type]['catalog_id']:
            catalog = ProductCatalog(data[campaign_type]['catalog_id'])
            if catalog:
                if data[campaign_type]['feed_id']:
                    print("Feed existing '%s'" % data[campaign_type]['feed_id'])
                else:
                    print("Feed not existing")
                    feed = catalog.create_product_feed(params=feed_params)
                    data[campaign_type]['feed_id'] = feed['id']
                    feed.create_upload(params={'url': feed_url})
                    print("Feed create '%s'" % data[campaign_type]['feed_id'])
    except FacebookRequestError as e:
        print(e._body.get('error', {}).get('message'))
        # print(e)
    except Exception as e:
        # print(e)
        pass


def create_product_set(campaign_type):
    setup_api_access()
    try:
        product_set_params = {'name': 'All lots test %s api call' % campaign_type,
                              'filter': {}}
        if data[campaign_type]['catalog_id']:
            catalog = ProductCatalog(data[campaign_type]['catalog_id'])
            if catalog:
                if data[campaign_type]['product_set_id']:
                    print("Product set existing '%s'" % data[campaign_type]['product_set_id'])
                else:
                    print("Product set not existing")
                    product_set = catalog.create_product_set(params=product_set_params)
                    data[campaign_type]['product_set_id'] = product_set['id']
                    print("Product creating '%s'" % data[campaign_type]['product_set_id'])
    except FacebookRequestError as e:
        print(e._body.get('error', {}).get('message'))
        # print(e)
    except Exception as e:
        # print(e)
        pass


def create_campaign(campaign_type):
    setup_api_access()
    try:
        params = get_params(campaign_type).get('campaign')
        acc = AdAccount('act_%s' % account_id)
        if data[campaign_type]['catalog_id']:
            if data[campaign_type]['campaign_id']:
                Campaign(data[campaign_type]['campaign_id']).api_update(fields=[], params=params)
                print("Campaign existing '%s'" % data[campaign_type]['campaign_id'])
            else:
                print("Campaign not existing")
                if acc:
                    campaign_result = acc.create_campaign(params=params)
                    data[campaign_type]['campaign_id'] = campaign_result['id']
                    print("Campaign creating '%s'" % data[campaign_type]['campaign_id'])
        else:
            print("Campaign Catalog not existing")
    except FacebookRequestError as e:
        print(e._body.get('error', {}).get('message'))
        # print(e)
    except Exception as e:
        # print(e)
        pass


def delete_campaign(campaign_type):
    setup_api_access()
    try:
        if data[campaign_type]['campaign_id']:
            campaign = Campaign(data[campaign_type]['campaign_id'])
            if campaign:
                campaign.api_delete()
                print("Campaign deleted '%s'" % data[campaign_type]['campaign_id'])
                data[campaign_type]['campaign_id'] = None
            else:
                print("Campaign not existing")
        else:
            print("Campaign not existing")
    except FacebookRequestError as e:
        print(e._body.get('error', {}).get('message'))
        # print(e)
    except Exception as e:
        # print(e)
        pass


def create_adset(campaign_type):
    setup_api_access()
    try:
        acc = AdAccount('act_%s' % account_id)
        params = get_params(campaign_type).get('adset')
        if data[campaign_type]['campaign_id']:
            if data[campaign_type]['adset_id']:
                AdSet(data[campaign_type]['adset_id']).api_update(fields=[], params=params)
                print("AdSet existing '%s'" % data[campaign_type]['adset_id'])
            else:
                print("AdSet not existing")
                adset_result = acc.create_ad_set(params=params)
                data[campaign_type]['adset_id'] = adset_result['id']
                print("AdSet creating '%s'" % data[campaign_type]['adset_id'])
        else:
            print("AdSet Campaign not existing")
    except FacebookRequestError as e:
        print(e._body.get('error', {}).get('message'))
        # print(e)
    except Exception as e:
        # print(e)
        pass


def delete_adset(campaign_type):
    setup_api_access()
    try:
        if data[campaign_type]['adset_id']:
            adset = AdSet(data[campaign_type]['adset_id'])
            if adset:
                adset.api_delete()
                print("AdSet deleted '%s'" % data[campaign_type]['adset_id'])
                data[campaign_type]['adset_id'] = None
            else:
                print("AdSet not existing")
        else:
            print("Campaign AdSet not existing")
    except FacebookRequestError as e:
        print(e._body.get('error', {}).get('message'))
        # print(e)
    except Exception as e:
        # print(e)
        pass


def create_ad_creative(campaign_type):
    setup_api_access()
    try:
        params = get_params(campaign_type).get('ad_creative')
        acc = AdAccount('act_%s' % account_id)
        if data[campaign_type]['ad_creative_id']:
            AdCreative(data[campaign_type]['ad_creative_id']).api_update(fields=[], params=params)
            print("Creative existing '%s'" % data[campaign_type]['ad_creative_id'])
        else:
            print("Creative not existing")
            if data[campaign_type]['campaign_id']:
                creative_result = acc.create_ad_creative(params=params)
                data[campaign_type]['ad_creative_id'] = creative_result['id']
                print("Creative creating '%s'" % data[campaign_type]['ad_creative_id'])
    except FacebookRequestError as e:
        print(e._body.get('error', {}).get('message'))
        # print(e)
    except Exception as e:
        # print(e)
        pass


def delete_ad_creative(campaign_type):
    setup_api_access()
    try:
        if data[campaign_type]['ad_creative_id']:
            ad_creative = AdCreative(data[campaign_type]['ad_creative_id'])
            if ad_creative:
                ad_creative.api_delete()
                print("Creative deleted '%s'" % data[campaign_type]['adset_id'])
                data[campaign_type]['ad_creative_id'] = None
            else:
                print("Creative not existing")
        else:
            print("Campaign Creative not existing")
    except FacebookRequestError as e:
        print(e._body.get('error', {}).get('message'))
        # print(e)
    except Exception as e:
        # print(e)
        pass


def create_ads(campaign_type):
    setup_api_access()
    try:
        acc = AdAccount('act_%s' % account_id)
        params = get_params(campaign_type).get('ads')
        if data[campaign_type]['ads_id']:
            Ad(data[campaign_type]['ads_id']).api_update(fields=[], params=params)
            print("Ads existing '%s'" % data[campaign_type]['ads_id'])
        else:
            print("Ads not existing")
            if data[campaign_type]['campaign_id'] and data[campaign_type]['adset_id'] and data[campaign_type][
                'ad_creative_id']:
                ads_result = acc.create_ad(params=params)
                data[campaign_type]['ads_id'] = ads_result['id']
                print("Ads creating '%s'" % data[campaign_type]['ads_id'])
    except FacebookRequestError as e:
        print(e._body.get('error', {}).get('message'))
        # print(e)
    except Exception as e:
        # print(e)
        pass


def delete_ads(campaign_type):
    setup_api_access()
    try:
        if data[campaign_type]['ads_id']:
            ads = Ad(data[campaign_type]['ads_id'])
            if ads:
                ads.api_delete()
                print("Ads deleted '%s'" % data[campaign_type]['ads_id'])
                data[campaign_type]['ads_id'] = None
            else:
                print("Ads not existing")
        else:
            print("Campaign Ads not existing")
    except FacebookRequestError as e:
        print(e._body.get('error', {}).get('message'))
        # print(e)
    except Exception as e:
        # print(e)
        pass


for z in range(0, 100):
    for item in ['new', 'rel', 'ret']:
        create_catalog(item)
        create_feed(item)
        create_product_set(item)
        for w in range(0, 5):
            for q in range(0, 2):
                create_campaign(item)
                create_adset(item)
                create_ad_creative(item)
                create_ads(item)

            delete_ads(item)
            delete_ad_creative(item)
            delete_adset(item)
            delete_campaign(item)

        delete_catalog(item)
    print('Complite %s' % z)
