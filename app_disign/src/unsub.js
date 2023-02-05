import React from 'react';
import ReactDOM from 'react-dom';
import {AppProvider} from '@shopify/polaris';
import '@shopify/polaris/styles.css';
import enTranslations from '@shopify/polaris/locales/en.json';
import UnsubApp from './UnsubApp';
import createApp from '@shopify/app-bridge';
import {Button, Redirect, TitleBar} from '@shopify/app-bridge/actions';
import SpinnerApp from './SpinnerApp';


ReactDOM.render(<SpinnerApp/>, document.getElementById('root'));

function WrappedApp(props) {
    return (
        <AppProvider i18n={enTranslations}>
            <UnsubApp current_shop={window.current_shop} redirect={props.redirect}/>
        </AppProvider>
    );
}

window.ga = window.ga || function () {
    (ga.q = ga.q || []).push(arguments)
};
ga.l = +new Date;


function getApp() {
    const app = createApp({
        apiKey: window.current_shop.apiKey,
        shopOrigin: window.current_shop.domain,
        host: new URLSearchParams(location.search).get("host"),
        forceRedirect: window.current_shop.forceRedirect,
        debug: window.current_shop.debug
    });
    return app;
}

function runApp() {
    const app = getApp();
    const redirect = Redirect.create(app);
    const subscribeButton = Button.create(app, {label: 'Upgrade to Premium Membershi'});
    const dashboard = Button.create(app, {label: 'Remain on premium membership'});
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
    dashboard.subscribe(Button.Action.CLICK, function () {
        const link = window.current_shop.dashboard;
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
        buttons.primary = dashboard;
    }
    const titleBarOptions = {
        title: window.current_shop.title,
        buttons: buttons
    };
    const myTitleBar = TitleBar.create(app, titleBarOptions);
    ReactDOM.render(<WrappedApp redirect={redirect}/>, document.getElementById('root'));
}

function inIframe() {
    try {
        return window.self !== window.top;
    } catch (e) {
        return true;
    }
}

if (window.current_shop.forceRedirect === false) {
    runApp();
}
else {
    if (inIframe()) {
        runApp();
    }
    else {
        setTimeout(getApp, 700)
    }

}