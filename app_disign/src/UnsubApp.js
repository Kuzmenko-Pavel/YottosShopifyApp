import React from 'react';
import {CalloutCard, Layout, Page} from '@shopify/polaris';
import {Redirect} from '@shopify/app-bridge/actions';

export default function App(props) {
    function remain() {
        props.redirect.dispatch(Redirect.Action.APP, props.current_shop.dashboard);
    }

    function downgrade() {
        props.redirect.dispatch(Redirect.Action.APP, props.current_shop.unsubscribe);
    }
    return (
        <Page>
            <Layout>
                <CalloutCard
                    title="Downgrade to free Membership"
                    illustration="/static/ARROW-DOWN.jpg"
                    primaryAction={{
                        content: 'Remain on premium membership',
                        onAction: remain
                    }}
                    secondaryAction={{
                        content: 'Downgrade to free Membership',
                        onAction: downgrade
                    }}
                >
                    <h2>FREE FOREVER SUBSCRIPTION PLAN</h2>
                    <p>Downgrading your subscription plan to free limited functions: </p>
                    <ul>
                        <li>Image enhancement limited to 50 images;</li>
                        <li>Synchronization of single collection;</li>
                        <li>Limited work to the following channels: Google, Facebook, Instagram, Yottos and Pinterest;
                        </li>
                        <li>Up to 1000 products in one collection;</li>
                        <li>Update your product feed manually every 48 hours.</li>
                    </ul>
                    <p>We recommend this subscription plan to introduce shopkeepers to our service and to test it’s
                        functions.</p>
                    <p>If you downgrade your subscription plan, you will lose access to PREMIUM functions, that will
                        make your campaigns more flexible and successful! </p>
                    <h2>ARE YOU SURE YOU WANT TO DOWNGRADE YOUR SUBSCRIPTION PLAN?</h2>
                </CalloutCard>
            </Layout>
        </Page>
    );
}
