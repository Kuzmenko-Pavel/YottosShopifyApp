import logging

from yottos_shopify.celery import app
from .models import FacebookCampaign, FacebookBusinessManager


token = 'EAAKUTF2LgQABAMDDg1nZAEa0CqG8EFCGuUQalGojYs82yoQNo0xd9dZAaWkkrx40vNkbUmpnFuhYyynQ3xs7wN0EH41MMxx15bXgrYDyZAcA02V6C8slQYtRLmaIHyfwYn8y9Cik7cki4IYzhJdI3V2FO6ZBZArA7mZBZCTb7jaowZDZD'


@app.task(ignore_result=True)
def fb_create_update(cid):
    try:
        camp = FacebookCampaign.objects.get(id=cid)
        camp.fb_get_or_create()
    except FacebookCampaign.DoesNotExist:
        logging.warning("non-existing campaign '%s'" % cid)


@app.task(ignore_result=True)
def fb_test_call_api():
    try:
        facebook = FacebookBusinessManager(
            myshopify_domain='cdn.yottos.com',
            access_token=token,
            business_id='183065162237916',
            account_id='210542543578120',
            pixel='217796929477510',
            page='105434934783882',
            connect=True
        )
        facebook.debug = True
        facebook.setup_access_token(token)
        facebook.save()

        for x in FacebookCampaign.CAMPAIGN_TYPE:
            campaign = FacebookCampaign(business=facebook,
                                        campaign_type=x[0],
                                        data={
                                            'geo': ["US"],
                                            'budget': 50.00,
                                            'status': True
                                        })
            campaign.save()
            campaign.facebookfeed_set.create(business=facebook)
            campaign.save()

            campaign.fb_get_or_create()

            campaign.paid = True

            campaign.fb_get_or_create()

        # facebook.delete()
    except Exception as e:
        logging.warning(e)
