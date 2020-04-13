import requests
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.user import User
from facebook_business.api import FacebookAdsApi

# short_access_token = 'EAAKUTF2LgQABANoIlZCidhALkqyVADwyd3TKIVsDDMU1RHtOBmdynpFeeOxatBblM1zzgIZAFEN6FhLnRpZCFDOnU2DbaLkk2zL3pT3rJ3CMu6kjX7rv305tIRnZC1LA8pAu0MFnCJGZBO0mCORZCv1DhRhkeQZCygoZAA3N7fAcdB1CThhl9Iwbk6y4mkiIyD6CKFYuDuA0ClLTgZB98YDZAmaW4VqmhEfVbZAZAvNpQxoGjVA7wnTuPLspLwKBVz4ZA5GwZD'
access_token = 'EAAKUTF2LgQABAN4dhpZAu5zNZAztm0glWYeeIVUXl8aLGjBx0ZAqJ1ZB6DsBZBUvL04mIutn9oh6kn4SRH7xgiED1ceZA5aDl3Nn8z4M32Ifmh3p4HYITtZCgLj4IJsvLZBfsiaIa6v9JtgDzGx5jdLZB02f563NyuBfEvRWiURS6Fe0szWapDunj'
app_secret = 'bc3c46925dc37a5a01549d791f81dc12'
app_id = '726005661270272'

r = requests.get('https://graph.facebook.com/%s/oauth/access_token?grant_type=fb_exchange_token&client_id=%s'
                 '&client_secret=%s&fb_exchange_token=%s' % ('v6.0', app_id, app_secret, access_token))
rd = r.json()
print(rd)
new_access_token = rd.get('access_token')
print(new_access_token == access_token)

new_access_token = 'EAAKUTF2LgQABAC3nibo5lwj9KQyNxFZBKSRzDdLCJ31waewRrgm8ZBD9Y7gDaO7YrLCtpRIl1ZBWjcd7KLE1R1GURx7WwJlsx5eZCqMQbVnEEVdtYAiOKobTu9ifyBvNYF63UB1eLXRPGxSKX00GH7ZCL0YQO8wQAu16PTZAEdEmrC2FTNbPEnZCSlw1VSiA0ZC2cmHLVwE78gZDZD'

FacebookAdsApi.init(access_token=new_access_token)
me = User(fbid='me').api_get(
    fields=[User.Field.email, User.Field.currency, User.Field.name, User.Field.timezone, User.Field.link])
print(me)
my_accounts = list(me.get_ad_accounts(fields=[AdAccount.Field.name]))
print(my_accounts)
my_business = list(me.get_businesses())
print(my_business)
