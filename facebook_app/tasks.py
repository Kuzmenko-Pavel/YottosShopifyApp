import logging

from yottos_shopify.celery import app
from .models import FacebookCampaign


@app.task(ignore_result=True)
def fb_create_update(cid):
    try:
        camp = FacebookCampaign.objects.get(id=cid)
        camp.fb_get_or_create()
        camp.save()
    except FacebookCampaign.DoesNotExist:
        logging.warning("non-existing campaign '%s'" % cid)
