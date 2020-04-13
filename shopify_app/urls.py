from django.urls import path

from . import views

app_name = 'shopify_app'
urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard/', views.Dashboard.as_view(), name='dashboard'),
    path('downgrade/', views.Downgrade.as_view(), name='downgrade'),
    path('dashboard/<str:feed>/', views.Dashboard.as_view(), name='dashboard_feeds'),
    path('install/', views.Install.as_view(), name='install'),
    path('authenticate/', views.Authenticate.as_view(), name='authenticate'),
    path('finalize/', views.Finalize.as_view(), name='finalize'),
    path('subscribe/', views.Subscribe.as_view(), name='subscribe'),
    path('unsubscribe/', views.UnSubscribe.as_view(), name='unsubscribe'),
    path('subscribe/submit', views.SubmitSubscribe.as_view(), name='subscribe_submit'),
    path('webhook/app_uninstalled/', views.WebhookAppUninstalled.as_view(), name='app_uninstalled'),
    path('gdpr/customers_redact/', views.WebhookGDPR.as_view(), name='gdpr_customers_redact'),
    path('gdpr/shop_redact/', views.WebhookGDPR.as_view(), name='gdpr_shop_redact'),
    path('gdpr/customers_data_request/', views.WebhookGDPR.as_view(), name='gdpr_customers_data_request'),
    path('proxy_url/', views.MainXml.as_view(), name='main_xml'),
    path('proxy_url/google.xml', views.GoogleXml.as_view(), name='google_xml'),
    path('proxy_url/facebook.xml', views.FacebookXml.as_view(), name='facebook_xml'),
    path('proxy_url/yottos.xml', views.YottosXml.as_view(), name='yottos_xml'),
    path('proxy_url/pinterest.xml', views.PinterestXml.as_view(), name='pinterest_xml'),
    path('save', views.save, name='save'),
    path('fb_integration', views.FbIntegration.as_view(), name='fb_integration'),
]
