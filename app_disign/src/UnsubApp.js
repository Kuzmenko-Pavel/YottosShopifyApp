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
                    <p>You will lose access to premium features.</p>
                </CalloutCard>
            </Layout>
        </Page>
    );
}
