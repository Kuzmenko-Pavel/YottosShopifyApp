import logging
from datetime import datetime, timedelta

import requests
from django.conf import settings
from django.db import models
from django.db.models.fields import BigIntegerField
from django_mysql.models import JSONField, Model
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


def camp_data():
    return {
        'geo': ["US"],
        'budget': 100,
        'status': False
    }


class FacebookBusinessManager(Model):
    myshopify_domain = models.CharField(max_length=100, help_text='Shopify store domain.', unique=True)
    user_id = BigIntegerField(null=True, blank=True)
    business_id = BigIntegerField(null=True, blank=True)
    account_id = BigIntegerField(null=True, blank=True)
    pixel = BigIntegerField(null=True, blank=True)
    page = BigIntegerField(null=True, blank=True)
    connect = models.BooleanField(help_text='App facebook connect.', default=False)
    access_token = models.TextField(help_text='Permanent token received from facebook.')
    access_token_end_date = models.DateTimeField(null=True, blank=True)

    def setup_access_token(self, token):
        r = requests.get('https://graph.facebook.com/%s/oauth/access_token?grant_type=fb_exchange_token&client_id=%s'
                         '&client_secret=%s&fb_exchange_token=%s' % ('v6.0', settings.FACEBOOK_APP_ID,
                                                                     settings.FACEBOOK_APP_SECRET, token
                                                                     ))
        rd = r.json()
        self.access_token = rd.get('access_token')
        self.access_token_end_date = datetime.now() + timedelta(seconds=rd.get('expires_in', 60 * 60 * 24 * 90))

    def setup_api_access(self):
        FacebookAdsApi.init(
            app_id=settings.FACEBOOK_APP_ID,
            app_secret=settings.FACEBOOK_APP_SECRET,
            access_token=self.access_token
        )


class FacebookCampaign(Model):
    CAMPAIGN_TYPE = (
        ('new', 'New Audience'),
        ('rel', 'Relevant Audience'),
        ('ret', 'Retargeting Audience'),

    )

    business = models.ForeignKey(FacebookBusinessManager, on_delete=models.CASCADE)
    campaign_id = BigIntegerField(null=True, blank=True)
    adset_id = BigIntegerField(null=True, blank=True)
    ad_creative_id = BigIntegerField(null=True, blank=True)
    ads_id = BigIntegerField(null=True, blank=True)
    paid = models.BooleanField(default=False)
    data = JSONField(default=camp_data)
    campaign_type = models.CharField(
        max_length=3,
        choices=CAMPAIGN_TYPE,
        default=CAMPAIGN_TYPE[0],
    )

    @property
    def get_params(self):
        product_set_id = None
        product_catalog_id = None
        for feed in self.facebookfeed_set.all():
            product_set_id = feed.product_set_id
            product_catalog_id = feed.catalog_id
        camp_status = Campaign.Status.paused
        adset_status = AdSet.Status.paused
        budget = int(self.data.get('budget', 15))
        budget = budget * 100
        countries = self.data.get('geo', ["US"])
        if len(countries) < 1:
            countries = ["US"]
            self.data['geo'] = ["US"]

        story = AdCreativeObjectStorySpec()
        story[story.Field.page_id] = self.business.page
        story[story.Field.template_data] = {
            "link": "https://%s/" % self.business.myshopify_domain,
            "name": "{{product.name}}",
            "description": "{{product.current_price strip_zeros}}",
            "call_to_action": {
                "type": "SHOP_NOW"
            },
            "multi_share_end_card": False,
            "show_multiple_images": False
        }
        story_ret = AdCreativeObjectStorySpec()
        story_ret[story.Field.page_id] = self.business.page
        story_ret[story.Field.template_data] = {
            "link": "https://%s/" % self.business.myshopify_domain,
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

        if self.data.get('status', False):
            camp_status = Campaign.Status.active
            # adset_status = AdSet.Status.active
        params = {
            self.CAMPAIGN_TYPE[0][0]: {
                'campaign': {
                    'name': 'Campaign %s %s (%s)' % (self.business.myshopify_domain,
                                                     self.get_campaign_type_display(),
                                                     self.id),
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
                    'name': 'AdSet %s %s (%s)' % (self.business.myshopify_domain,
                                                  self.get_campaign_type_display(),
                                                  self.id),
                    'bid_strategy': AdSet.BidStrategy.lowest_cost_without_cap,
                    'billing_event': AdSet.BillingEvent.impressions,
                    'campaign_id': self.campaign_id,
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
                        "pixel_id": self.business.pixel
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
                    'name': 'Ad Template %s %s (%s)' % (self.business.myshopify_domain,
                                                        self.get_campaign_type_display(),
                                                        self.id),
                    AdCreative.Field.object_story_spec: story,
                    AdCreative.Field.product_set_id: product_set_id,
                    # AdCreative.Field.call_to_action_type: AdCreative.CallToActionType.shop_now,
                    AdCreative.Field.object_type: AdCreative.ObjectType.share,
                    AdCreative.Field.title: "{{product.name}}",
                },
                'ads': {
                    Ad.Field.name: 'Ad %s %s (%s)' % (self.business.myshopify_domain,
                                                      self.get_campaign_type_display(),
                                                      self.id),
                    Ad.Field.adset_id: self.adset_id,
                    Ad.Field.creative: {'creative_id': self.ad_creative_id},
                    Ad.Field.status: adset_status,
                    Ad.Field.tracking_specs: [
                        {
                            "action.type": [
                                "offsite_conversion"
                            ],
                            "fb_pixel": [
                                self.business.pixel
                            ]
                        },
                        {
                            "action.type": [
                                "post_engagement"
                            ],
                            "page": [
                                self.business.page
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
                                self.business.page
                            ]
                        }
                    ]
                }
            },
            self.CAMPAIGN_TYPE[1][0]: {
                'campaign': {
                    'name': 'Campaign %s %s (%s)' % (self.business.myshopify_domain,
                                                     self.get_campaign_type_display(),
                                                     self.id),
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
                    'name': 'AdSet %s %s (%s)' % (self.business.myshopify_domain,
                                                  self.get_campaign_type_display(),
                                                  self.id),
                    'bid_strategy': AdSet.BidStrategy.lowest_cost_without_cap,
                    'billing_event': AdSet.BillingEvent.impressions,
                    'campaign_id': self.campaign_id,
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
                        "pixel_id": self.business.pixel
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
                    'name': 'Ad Template %s %s (%s)' % (self.business.myshopify_domain,
                                                        self.get_campaign_type_display(),
                                                        self.id),
                    AdCreative.Field.object_story_spec: story,
                    AdCreative.Field.product_set_id: product_set_id,
                    # AdCreative.Field.call_to_action_type: AdCreative.CallToActionType.shop_now,
                    AdCreative.Field.object_type: AdCreative.ObjectType.share,
                    AdCreative.Field.title: "{{product.name}}",
                },
                'ads': {
                    Ad.Field.name: 'Ad %s %s (%s)' % (self.business.myshopify_domain,
                                                      self.get_campaign_type_display(),
                                                      self.id),
                    Ad.Field.adset_id: self.adset_id,
                    Ad.Field.creative: {'creative_id': self.ad_creative_id},
                    Ad.Field.status: adset_status,
                    Ad.Field.tracking_specs: [
                        {
                            "action.type": [
                                "offsite_conversion"
                            ],
                            "fb_pixel": [
                                self.business.pixel
                            ]
                        },
                        {
                            "action.type": [
                                "post_engagement"
                            ],
                            "page": [
                                self.business.page
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
                                self.business.page
                            ]
                        }
                    ]
                }
            },
            self.CAMPAIGN_TYPE[2][0]: {
                'campaign': {
                    'name': 'Campaign %s %s (%s)' % (self.business.myshopify_domain,
                                                     self.get_campaign_type_display(),
                                                     self.id),
                    'objective': Campaign.Objective.product_catalog_sales,
                    'special_ad_category': Campaign.SpecialAdCategory.none,
                    'status': camp_status,
                    'can_use_spend_cap': True,
                    'can_create_brand_lift_study': False,
                    'buying_type': "AUCTION",
                    "budget_remaining": "0",
                    "budget_rebalance_flag": False,
                    'promoted_object': {
                        "product_catalog_id": product_catalog_id
                    },
                },
                'adset': {
                    'name': 'AdSet %s %s (%s)' % (self.business.myshopify_domain,
                                                  self.get_campaign_type_display(),
                                                  self.id),
                    'bid_strategy': AdSet.BidStrategy.lowest_cost_without_cap,
                    'billing_event': AdSet.BillingEvent.impressions,
                    'campaign_id': self.campaign_id,
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
                        "product_set_id": product_set_id
                    },
                    "targeting": {
                        Targeting.Field.age_max: 65,
                        Targeting.Field.age_min: 22,
                        Targeting.Field.product_audience_specs: [
                            {
                                "product_set_id": product_set_id,
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
                    'name': 'Ad Template %s %s (%s)' % (self.business.myshopify_domain,
                                                        self.get_campaign_type_display(),
                                                        self.id),
                    AdCreative.Field.object_story_spec: story_ret,
                    AdCreative.Field.product_set_id: product_set_id,
                    # AdCreative.Field.call_to_action_type: AdCreative.CallToActionType.shop_now,
                    AdCreative.Field.object_type: AdCreative.ObjectType.share,
                    AdCreative.Field.title: "{{product.name}}",
                },
                'ads': {
                    Ad.Field.name: 'Ad %s %s (%s)' % (self.business.myshopify_domain,
                                                      self.get_campaign_type_display(),
                                                      self.id),
                    Ad.Field.adset_id: self.adset_id,
                    Ad.Field.creative: {'creative_id': self.ad_creative_id},
                    Ad.Field.status: adset_status,
                    Ad.Field.tracking_specs: [
                        {
                            "action.type": [
                                "offsite_conversion"
                            ],
                            "fb_pixel": [
                                self.business.pixel
                            ]
                        },
                        {
                            "action.type": [
                                "post_engagement"
                            ],
                            "page": [
                                self.business.page
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
                                self.business.page
                            ]
                        }
                    ]
                }
            }
        }
        return params[self.campaign_type]

    def fb_get_or_create(self):
        self.business.setup_api_access()
        try:
            for feed in self.facebookfeed_set.all():
                feed.fb_get_or_create()

            params = self.get_params.get('campaign')
            if self.paid:
                acc = AdAccount('act_%s' % self.business.account_id)
                if self.campaign_id:
                    print(Campaign(self.campaign_id).api_update(fields=[], params=params))
                    logging.warning("Campaign existing '%s'" % self.campaign_id)
                else:
                    logging.warning("Campaign not existing")
                    if acc:
                        campaign_result = acc.create_campaign(params=params)
                        self.campaign_id = campaign_result['id']
                        logging.warning("Campaign creating '%s'" % self.campaign_id)
        except FacebookRequestError as e:
            logging.warning(e._body.get('error_user_msg', e._body))
            print(e)
        except Exception as e:
            print(e)

        self.fb_get_or_create_adset()
        self.save(update_fields=['campaign_id', 'adset_id', 'ad_creative_id', 'ads_id'])

    def fb_get_or_create_adset(self):
        self.business.setup_api_access()
        try:
            acc = AdAccount('act_%s' % self.business.account_id)
            params = self.get_params.get('adset')
            if self.adset_id:
                print(AdSet(self.adset_id).api_update(fields=[], params=params))
                logging.warning("AdSet existing '%s'" % self.adset_id)
            else:
                logging.warning("AdSet not existing")
                if self.campaign_id:
                    adset_result = acc.create_ad_set(params=params)
                    self.adset_id = adset_result['id']
                    logging.warning("AdSet creating '%s'" % self.adset_id)
        except FacebookRequestError as e:
            logging.warning(e._body.get('error_user_msg', e._body))
            print(e)
        except Exception as e:
            print(e)

        self.fb_get_or_create_ad_creative()

    def fb_get_or_create_ad_creative(self):
        self.business.setup_api_access()
        try:
            params = self.get_params.get('ad_creative')
            acc = AdAccount('act_%s' % self.business.account_id)
            if self.ad_creative_id:
                print(AdCreative(self.ad_creative_id).api_update(fields=[], params=params))
                logging.warning("Creative existing '%s'" % self.ad_creative_id)
            else:
                logging.warning("Creative not existing")
                if self.campaign_id:
                    creative_result = acc.create_ad_creative(params=params)
                    self.ad_creative_id = creative_result['id']
                    logging.warning("Creative creating '%s'" % self.ad_creative_id)
        except FacebookRequestError as e:
            logging.warning(e._body.get('error_user_msg', e._body))
            print(e)
        except Exception as e:
            print(e)
        self.fb_get_or_create_ads()

    def fb_get_or_create_ads(self):
        self.business.setup_api_access()
        try:
            acc = AdAccount('act_%s' % self.business.account_id)
            params = self.get_params.get('ads')
            if self.ads_id:
                print(Ad(self.ads_id).api_update(fields=[], params=params))
                logging.warning("Ads existing '%s'" % self.ads_id)
            else:
                logging.warning("Ads not existing")
                if self.campaign_id and self.adset_id and self.ad_creative_id:
                    ads_result = acc.create_ad(params=params)
                    self.ads_id = ads_result['id']
                    logging.warning("Ads creating '%s'" % self.ads_id)
        except FacebookRequestError as e:
            logging.warning(e._body.get('error_user_msg', e._body))
            print(e)
        except Exception as e:
            print(e)


class FacebookFeed(Model):
    business = models.ForeignKey(FacebookBusinessManager, on_delete=models.CASCADE)
    campaign = models.ForeignKey(FacebookCampaign, on_delete=models.CASCADE, default=None)
    feed_id = BigIntegerField(null=True, blank=True)
    catalog_id = BigIntegerField(null=True, blank=True)
    product_set_id = BigIntegerField(null=True, blank=True)

    def fb_get_or_create(self):
        try:
            self.business.setup_api_access()
            try:
                catalog_params = {
                    'name': 'Catalog %s %s (%s)' % (self.business.myshopify_domain,
                                                    self.campaign.get_campaign_type_display(),
                                                    self.id),
                }

                acc = Business(self.business.business_id)
                if self.catalog_id:
                    logging.warning("Catalog existing '%s'" % self.catalog_id)
                else:
                    logging.warning("Catalog not existing")
                    catalog = acc.create_owned_product_catalog(
                        params=catalog_params
                    )
                    catalog.add_external_event_sources(pixel_ids=[self.business.pixel, ])
                    self.catalog_id = catalog['id']
                    logging.warning("Catalog creating '%s'" % self.catalog_id)
            except FacebookRequestError as e:
                logging.warning(e._body.get('error_user_msg', e._body))
                print(e)
            except Exception as e:
                print(e)

            self.fb_feed_get_or_create()
            self.fb_product_set_get_or_create()
            self.save(update_fields=['catalog_id', 'feed_id', 'product_set_id'])
        except FacebookRequestError as e:
            logging.warning(e._body.get('error_user_msg', e._body))
            print(e)
        except Exception as e:
            print(e)

    def fb_feed_get_or_create(self):
        try:
            self.business.setup_api_access()
            feed_url = 'https://%s/%s.xml' % (self.business.myshopify_domain, 'a/ytt_feed/facebook.xml')
            feed_url = 'https://cdn.yottos.com/sf.xml'
            feed_params = {
                'name': 'Feed %s %s (%s)' % (self.business.myshopify_domain,
                                             self.campaign.get_campaign_type_display(),
                                             self.id),
                'schedule': {'interval': 'DAILY',
                             'url': feed_url,
                             'hour': '22'},
            }
            if self.catalog_id:
                catalog = ProductCatalog(self.catalog_id)
                if catalog:
                    if self.feed_id:
                        logging.warning("Feed existing '%s'" % self.feed_id)
                    else:
                        logging.warning("Feed not existing")
                        feed = catalog.create_product_feed(params=feed_params)
                        self.feed_id = feed['id']
                        feed.create_upload(params={'url': feed_url})
                        logging.warning("Feed create '%s'" % self.feed_id)
        except FacebookRequestError as e:
            logging.warning(e._body.get('error_user_msg', e._body))
            print(e)
        except Exception as e:
            print(e)

    def fb_product_set_get_or_create(self):
        try:
            self.business.setup_api_access()
            product_set_params = {'name': 'All lots %s %s (%s)' % (self.business.myshopify_domain,
                                                                   self.campaign.get_campaign_type_display(),
                                                                   self.id),
                                  'filter': {}}
            if self.catalog_id:
                catalog = ProductCatalog(self.catalog_id)
                if catalog:
                    if self.product_set_id:
                        logging.warning("Product set existing '%s'" % self.product_set_id)
                    else:
                        logging.warning("Product set not existing")
                        product_set = catalog.create_product_set(params=product_set_params)
                        self.product_set_id = product_set['id']
                        logging.warning("Product creating '%s'" % self.product_set_id)
        except FacebookRequestError as e:
            logging.warning(e._body.get('error_user_msg', e._body))
            print(e)
        except Exception as e:
            print(e)
