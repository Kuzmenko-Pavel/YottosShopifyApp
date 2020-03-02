import React from 'react';
import {CalloutCard, Layout, Page} from '@shopify/polaris';

export default function App(props) {
    return (
        <Page>
            <Layout>
                <CalloutCard
                    title="Downgrade to free Membership"
                    illustration="/static/ARROW-DOWN.jpg"
                    primaryAction={{content: 'Remain on premium membership'}}
                    secondaryAction={{
                        content: 'Downgrade to free Membership'
                    }}
                >
                    <p>You will lose access to premium features.</p>
                </CalloutCard>
            </Layout>
        </Page>
    );
}
