import React from 'react';
import ReactDOM from 'react-dom';
import {AppProvider, Spinner} from '@shopify/polaris';
import enTranslations from '@shopify/polaris/locales/en.json';
import '@shopify/polaris/styles.css';

import IntegrationApp from './IntegrationApp';
import createApp from '@shopify/app-bridge';
import {Button, Redirect, TitleBar} from '@shopify/app-bridge/actions';

function SpinnerApp() {
    return (
        <AppProvider i18n={enTranslations}>
            <div style={{
                position: 'absolute',
                left: '50%',
                top: '50%'
            }}>
                <Spinner size="large" color="teal"/>
            </div>
        </AppProvider>
    );
}

function WrappedApp(props) {
    return (
        <AppProvider i18n={enTranslations}>
            <IntegrationApp current_shop={window.current_shop} redirect={props.redirect} businesses={props.businesses}/>
        </AppProvider>
    );
}

window.ga = window.ga || function () {
    (ga.q = ga.q || []).push(arguments)
};
ga.l = +new Date;

const app = createApp({
    apiKey: window.current_shop.apiKey,
    shopOrigin: window.current_shop.domain,
    forceRedirect: window.current_shop.forceRedirect,
    debug: window.current_shop.debug
});
const redirect = Redirect.create(app);
const subscribeButton = Button.create(app, {label: 'Upgrade to Premium Membershi'});
const unSubscribeButton = Button.create(app, {label: 'Downgrade to free Membership'});
const button1 = Button.create(app, {label: 'Facebook (Instagram) Feed'});
const button2 = Button.create(app, {label: 'Google Feed'});
const button3 = Button.create(app, {label: 'Yottos Feed'});
const button4 = Button.create(app, {label: 'Pinterest Feed'});
subscribeButton.subscribe(Button.Action.CLICK, function () {
    window.ga('send', 'event', 'Order', 'Upgrade', 'BigButton');
    window.ga('ec:addProduct', {
        'id': '1',
        'name': 'Premium',
        'price': '29.00',
        'variant': 'BigButton',
        'quantity': 1
    });
    // Add the step number and additional info about the checkout to the action.
    window.ga('ec:setAction', 'checkout', {
        'step': 1,
        'id': window.t
    });
    if (window.fbq) {
        fbq('track', 'InitiateCheckout', {
            content_ids: [1],
            content_name: 'Premium',
            content_type: 'product',
            content_category: 'BigButton',
            contents: [
                {
                    'id': '1',
                    'quantity': 1
                }
            ],
            currency: "USD",
            value: 29.00
        });
    }
    const link = window.current_shop.billing;
    redirect.dispatch(Redirect.Action.APP, link);
});
unSubscribeButton.subscribe(Button.Action.CLICK, function () {
    window.ga('send', 'event', 'Order', 'Downgrade', 'BigButton');
    const link = window.current_shop.downgrade;
    redirect.dispatch(Redirect.Action.APP, link);
});
button1.subscribe(Button.Action.CLICK, function () {
    ReactDOM.render(<SpinnerApp/>, document.getElementById('root'));
    window.ga('send', 'event', 'Feed', 'Open', 'Facebook');
    const link = window.current_shop.dashboard + 'fb/';
    redirect.dispatch(Redirect.Action.APP, link);
});
button2.subscribe(Button.Action.CLICK, function () {
    ReactDOM.render(<SpinnerApp/>, document.getElementById('root'));
    window.ga('send', 'event', 'Feed', 'Open', 'Google');
    const link = window.current_shop.dashboard + 'ga/';
    redirect.dispatch(Redirect.Action.APP, link);
});
button3.subscribe(Button.Action.CLICK, function () {
    ReactDOM.render(<SpinnerApp/>, document.getElementById('root'));
    window.ga('send', 'event', 'Feed', 'Open', 'Yottos');
    const link = window.current_shop.dashboard + 'yt/';
    redirect.dispatch(Redirect.Action.APP, link);
});
button4.subscribe(Button.Action.CLICK, function () {
    ReactDOM.render(<SpinnerApp/>, document.getElementById('root'));
    window.ga('send', 'event', 'Feed', 'Open', 'Pinterest');
    const link = window.current_shop.dashboard + 'pi/';
    redirect.dispatch(Redirect.Action.APP, link);
});
const pathname = document.location.pathname;
if (pathname.includes('/fb/')) {
    button1.disabled = true;
}
else if (pathname.includes('/ga/')) {
    button2.disabled = true;
}
else if (pathname.includes('/yt/')) {
    button3.disabled = true;
}
else if (pathname.includes('/pi/')) {
    button4.disabled = true;
}
const buttons = {
    secondary: [
        button1,
        button2,
        button3,
        button4
    ]
};
if (!window.current_shop.premium) {
    buttons.primary = subscribeButton;
}
else {
    buttons.primary = unSubscribeButton;
}
const titleBarOptions = {
    title: window.current_shop.title,
    buttons: buttons
};
const myTitleBar = TitleBar.create(app, titleBarOptions);
let businesses = [];

function zstatusChangeCallback(response) {
    if (response.status === 'connected') {
        FB.api('me/businesses?fields=id,name,owned_ad_accounts{account_id,name,account_status,adspixels{name}}', function (response) {
            console.log(response);
                (response.data || []).forEach(
                    businesse => {
                        let obj = {
                            label: businesse.name,
                            value: businesse.id,
                            accounts: []
                        };
                        ((businesse.owned_ad_accounts || {}).data || []).forEach(
                            account => {
                                let obj_account = {
                                    label: account.name,
                                    value: account.account_id,
                                    pixels: []
                                };
                                ((account.adspixels || {}).data || []).forEach(
                                    pixel => obj_account.pixels.push({
                                        label: pixel.name,
                                        value: pixel.id
                                    }));
                                obj.accounts.push(obj_account);
                            });
                        businesses.push(obj);
                    }
                );
                ReactDOM.render(<WrappedApp redirect={redirect} businesses={businesses}/>, document.getElementById('root'));
            }
        );
    } else {
        const link = window.current_shop.dashboard;
        redirect.dispatch(Redirect.Action.APP, link);
    }
}

function connectFb() {
    FB.getLoginStatus(function (response) {   // See the onlogin handler
        statusChangeCallback(response);
    });
}

window.fbAsyncInit = function () {
    console.log('fbAsyncInit');
    FB.init({
        appId: '726005661270272',
        cookie: true,
        xfbml: false,
        status: true,
        version: 'v6.0'
    });
    connectFb()
};
ReactDOM.render(<SpinnerApp/>, document.getElementById('root'));