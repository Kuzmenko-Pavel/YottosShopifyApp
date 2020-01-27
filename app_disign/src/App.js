import React, {Component, useCallback, useState} from 'react';
import {Layout, Page} from '@shopify/polaris';
import Feed from './Feed';
import Options from './Options';
import UTM from './Utm';
import Collections from './Collections';

export default function App() {
    return (
        <Page>
            <Layout>
                <Feed current_shop={window.current_shop} />
                <Collections current_shop={window.current_shop}></Collections>
                <UTM current_shop={window.current_shop}></UTM>
                <Options current_shop={window.current_shop} />
            </Layout>
        </Page>
    );
}
