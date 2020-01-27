import React from 'react';
import {Layout, Page} from '@shopify/polaris';
import Feed from './Feed';
import Options from './Options';
import UTM from './Utm';
import Collections from './Collections';

export default function App(props) {
    return (
        <Page>
            <Layout>
                <Feed current_shop={window.current_shop} redirect={props.redirect} />
                <Collections current_shop={window.current_shop} redirect={props.redirect} />
                <UTM current_shop={window.current_shop} redirect={props.redirect} />
                <Options current_shop={window.current_shop} redirect={props.redirect}/>
            </Layout>
        </Page>
    );
}
