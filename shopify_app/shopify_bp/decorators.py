import re
from functools import wraps
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound

import shopify
from flask import session, redirect, url_for, request, current_app

from ..extensions import db
from .models import Shop

shop_name_pattern = re.compile("[a-zA-Z0-9][a-zA-Z0-9\-]*\.myshopify\.com[\/]?")


def shopify_auth_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "shopify_token" not in session:
            shop_url = request.args.get('shop')
            shop = None
            try:
                shop = Shop.query.filter_by(shop=shop_url).one()
            except NoResultFound:
                return redirect(url_for('shopify_bp.install', **request.args))

            shopify.Session.setup(
                api_key=current_app.config['SHOPIFY_API_KEY'],
                secret=current_app.config['SHOPIFY_SHARED_SECRET'])
            try:
                shopify_session = shopify.Session.validate_params(request.args)
                shopify.ShopifyResource.activate_session(shopify_session)
                shopify.Shop.current()
            except Exception:
                if shop:
                    shop.delete()
                return redirect(url_for('shopify_bp.install', **request.args))

            session['shopify_token'] = shop.token
            session['shopify_url'] = shop_url
            session['shopify_id'] = shop.id

        else:
            try:
                shop = Shop.query.filter_by(shop=session['shopify_url']).one()
                shopify_session = shopify.Session(shop.shop, token=shop.token,
                                                  version=current_app.config['SHOPIFY_API_VERSION'])
                shopify.ShopifyResource.activate_session(shopify_session)
                shopify.Shop.current()
            except NoResultFound:
                session.pop("shopify_token")
                session.pop("shopify_url")
                session.pop("shopify_id")
                return redirect(url_for('shopify_bp.install', **request.args))
            except MultipleResultsFound:
                Shop.query.filter_by(shop=session['shopify_url']).delete()
                db.session.commit()
                session.pop("shopify_token")
                session.pop("shopify_url")
                session.pop("shopify_id")
                return redirect(url_for('shopify_bp.install', **request.args))
            except Exception:
                session.pop("shopify_token")
                session.pop("shopify_url")
                session.pop("shopify_id")
                return redirect(url_for('shopify_bp.install', **request.args))

        return f(*args, **kwargs)

    return decorated_function


def shopify_check_shop_name(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        shop_url = request.args.get("shop")
        if shop_url and shop_name_pattern.match(shop_url) is None:
            return redirect(url_for('shopify_bp.install', **request.args))

        return f(*args, **kwargs)

    return decorated_function
