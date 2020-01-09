import shopify
from flask import (
    Blueprint, render_template, current_app, request, redirect, session,
    url_for)

from .decorators import shopify_auth_required, shopify_check_shop_name
from .models import Shop
from ..extensions import db

shopify_bp = Blueprint('shopify_bp', __name__, url_prefix='/shopify')


@shopify_bp.route('/')
@shopify_check_shop_name
@shopify_auth_required
def index():
    """ Render the index page of our application.

    """

    return render_template('shopify_bp/index.html')


@shopify_bp.route('/install')
@shopify_check_shop_name
def install():
    """ Redirect user to permission authorization page.

    """

    shop_url = request.args.get("shop")

    shopify.Session.setup(
        api_key=current_app.config['SHOPIFY_API_KEY'],
        secret=current_app.config['SHOPIFY_SHARED_SECRET'])

    session = shopify.Session(shop_url, version=current_app.config['SHOPIFY_API_VERSION'])

    scope = [
        "write_products", "read_products", "read_script_tags",
        "write_script_tags", "read_orders", "write_orders"]
    redirect_uri = url_for("shopify_bp.finalize", _external=True, _scheme=current_app.config['PREFERRED_URL_SCHEME'])
    permission_url = session.create_permission_url(scope, redirect_uri)

    return render_template('shopify_bp/install.html', permission_url=permission_url)


@shopify_bp.route('/finalize')
@shopify_check_shop_name
def finalize():
    """ Generate shop token and store the shop information.
    
    """

    shop_url = request.args.get("shop")
    shopify.Session.setup(
        api_key=current_app.config['SHOPIFY_API_KEY'],
        secret=current_app.config['SHOPIFY_SHARED_SECRET'])
    shopify_session = shopify.Session(shop_url, version=current_app.config['SHOPIFY_API_VERSION'])

    token = shopify_session.request_token(request.args)

    shop = Shop(shop=shop_url, token=token)
    shop.save()

    session['shopify_url'] = shop_url
    session['shopify_token'] = token
    session['shopify_id'] = shop.id

    return redirect(url_for('shopify_bp.index'))
