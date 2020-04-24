"""shopify_app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path, include

from yottos_shopify import views

urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('privacy.html', views.Privacy.as_view()),
    path('cookie-policy.html', views.Cookie.as_view()),
    path('help_center.html', views.FAQ.as_view(), name='help_center'),
    path('help_center/how_install.html', views.HowInstall.as_view()),
    path('help_center/how_configure.html', views.HowConfigure.as_view()),
    path('help_center/how_setup_google_merchant_feed.html', views.HowSetupGoogle.as_view()),
    path('help_center/how_setup_facebook_catalog_feed.html', views.HowSetupFacebook.as_view()),
    path('help_center/how_setup_instagram_feed.html', views.HowSetupInstagram.as_view()),
    path('help_center/how_setup_yottos_adload_feed.html', views.HowSetupYottos.as_view()),
    path('help_center/how_setup_pinterest_feed.html', views.HowSetupPinterest.as_view()),
    path('help_center/how_create_facebook_pixel.html', views.HowCreateFacebookPixel.as_view()),
    path('help_center/upload_products_in_facebook_store.html', views.UploadProductsInFacebookStore.as_view()),
    path('help_center/dynamic_remarketing_in_facebook.html', views.DynamicRemarketingInFacebook.as_view()),
    path('help_center/strategies_in_feed_product.html', views.StrategiesInFeedProduct.as_view()),
    path('admin/', admin.site.urls),
    path('shopify/', include('shopify_app.urls')),
    path('facebook/', include('facebook_app.urls')),
]


def response_error_handler(request, exception=None):
    print(request)
    print(exception)
    return redirect('/')

# handler404 = response_error_handler
# handler500 = response_error_handler
