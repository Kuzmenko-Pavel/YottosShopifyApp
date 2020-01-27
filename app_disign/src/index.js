import React from 'react';
import ReactDOM from 'react-dom';
import {AppProvider, Spinner} from '@shopify/polaris';
import enTranslations from '@shopify/polaris/locales/en.json';
import '@shopify/polaris/styles.css';

import App from './App';
import createApp from '@shopify/app-bridge';
import {Button, Redirect, TitleBar} from '@shopify/app-bridge/actions';

function SpinnerApp() {
    return (
        <AppProvider i18n={enTranslations}>
            {/*<Spinner accessibilityLabel="Spinner example" size="large" color="teal"/>*/}
        </AppProvider>
    );
}

function WrappedApp(props) {
    return (
        <AppProvider i18n={enTranslations}>
            <App redirect={props.redirect}/>
        </AppProvider>
    );
}

const app = createApp({
    apiKey: window.current_shop.apiKey,
    shopOrigin: window.current_shop.domain,
    forceRedirect: window.current_shop.forceRedirect,
    debug: window.current_shop.debug
});
const redirect = Redirect.create(app);
const subscribeButton = Button.create(app, {label: 'Upgrade to Premium Membershi'});
const button1 = Button.create(app, {label: 'Facebook Feed'});
const button2 = Button.create(app, {label: 'Google Feed'});
const button3 = Button.create(app, {label: 'Yottos Feed'});
const button4 = Button.create(app, {label: 'Pinterest Feed'});
subscribeButton.subscribe(Button.Action.CLICK, function () {
    const link = window.current_shop.billing;
    redirect.dispatch(Redirect.Action.APP, link);
});
button1.subscribe(Button.Action.CLICK, function () {
    ReactDOM.render(<SpinnerApp/>, document.getElementById('root'));
    const link = window.current_shop.dashboard + 'fb/';
    redirect.dispatch(Redirect.Action.APP, link);
});
button2.subscribe(Button.Action.CLICK, function () {
    ReactDOM.render(<SpinnerApp/>, document.getElementById('root'));
    const link = window.current_shop.dashboard + 'ga/';
    redirect.dispatch(Redirect.Action.APP, link);
});
button3.subscribe(Button.Action.CLICK, function () {
    ReactDOM.render(<SpinnerApp/>, document.getElementById('root'));
    const link = window.current_shop.dashboard + 'yt/';
    redirect.dispatch(Redirect.Action.APP, link);
});
button4.subscribe(Button.Action.CLICK, function () {
    ReactDOM.render(<SpinnerApp/>, document.getElementById('root'));
    const link = window.current_shop.dashboard + 'pi/';
    redirect.dispatch(Redirect.Action.APP, link);
});

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
const titleBarOptions = {
    title: window.current_shop.title,
    buttons: buttons
};
const myTitleBar = TitleBar.create(app, titleBarOptions);
ReactDOM.render(<WrappedApp redirect={redirect}/>, document.getElementById('root'));
