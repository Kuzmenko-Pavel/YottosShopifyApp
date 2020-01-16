from .helpers import ShopifyHelper
from background_task import background


# @background(schedule=30)
# def task_first_run(shop_url):
#     store = ShopifyHelper(shop_url)
#     store.activate_session()
#     store.bulk_add_products()
#     store.bulk_add_variants()
#     store.create_webhook()
#     store.clear_session()
#     print('Done!')


@background()
def app_uninstalled(data):
    shop_url = data.get('X-Shopify-Shop-Domain')
    print('Task: App Uninstalled completed successfully.')
