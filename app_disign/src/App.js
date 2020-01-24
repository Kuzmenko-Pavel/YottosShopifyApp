import React, {Component, useCallback, useState} from 'react';
import {Layout, Page} from '@shopify/polaris';
import Feed from './Feed';
import Options from './Options';

export default function App() {
    let current_shop = window.current_shop;

    return (
        <Page>
            <Layout>
                <Feed current_shop={current_shop} />
                <Options current_shop={current_shop} />
            </Layout>
        </Page>
    );
}
