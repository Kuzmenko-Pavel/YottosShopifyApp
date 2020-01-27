import React from 'react';
import ReactDOM from 'react-dom';
import {AppProvider} from '@shopify/polaris';
import enTranslations from '@shopify/polaris/locales/en.json';
import '@shopify/polaris/styles.css';
import BillingApp from './BillingApp';

function WrappedApp() {
    return (
        <AppProvider i18n={enTranslations}>
            <BillingApp/>
        </AppProvider>
    );
}

ReactDOM.render(<WrappedApp/>, document.getElementById('root'));
