import React from 'react';
import {Layout, Page} from '@shopify/polaris';
import Feed from './Feed';
import Options from './Options';
import UTM from './Utm';
import Collections from './Collections';
import createApp from '@shopify/app-bridge';
import {Button, TitleBar, Redirect} from '@shopify/app-bridge/actions';

export default function App() {
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
    const clickSubscribe = subscribeButton.subscribe(Button.Action.CLICK, function () {
        redirect.dispatch(Redirect.Action.APP, window.current_shop.billing);
    });
    const clickButton1 = button1.subscribe(Button.Action.CLICK, function () {
        redirect.dispatch(Redirect.Action.APP, window.current_shop.dashboard + '?feed=fb');
    });
    const clickButton2 = button2.subscribe(Button.Action.CLICK, function () {
        redirect.dispatch(Redirect.Action.APP, window.current_shop.dashboard + '?feed=ga');
    });
    const clickButton3 = button3.subscribe(Button.Action.CLICK, function () {
        redirect.dispatch(Redirect.Action.APP, window.current_shop.dashboard + '?feed=yt');
    });
    const clickButton4 = button4.subscribe(Button.Action.CLICK, function () {
        redirect.dispatch(Redirect.Action.APP, window.current_shop.dashboard + '?feed=pi');
    });

    const buttons = {
        secondary: [
                button1,
                button2,
                button3,
                button4
            ]
    };
    if(!window.current_shop.premium){
        buttons.primary = subscribeButton;
    }
    const titleBarOptions = {
        title: window.current_shop.title,
        buttons: buttons
    };
    const myTitleBar = TitleBar.create(app, titleBarOptions);
    console.log(myTitleBar);
    app.getState().then((data) => {
      const {appInfo, loading, modal, navigation, pos, resourcePicker, staffMember, titleBar, toast} = data;
      console.log(appInfo, loading, modal, navigation, pos, resourcePicker, staffMember, titleBar, toast);
    });
    return (
        <Page>
            <Layout>
                <Feed current_shop={window.current_shop} redirect={redirect} />
                <Collections current_shop={window.current_shop} redirect={redirect} />
                <UTM current_shop={window.current_shop} redirect={redirect} />
                <Options current_shop={window.current_shop} redirect={redirect}/>
            </Layout>
        </Page>
    );
}
