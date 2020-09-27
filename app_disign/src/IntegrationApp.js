import React, {useCallback, useState} from 'react';

import {Card, Layout, Page, Tabs} from '@shopify/polaris';

import Choicer from './integration_components/Choicer';
import ChoicerFunding from './integration_components/ChoicerFunding';
import * as Redirect from "@shopify/app-bridge/actions/Navigation/Redirect";
import axios from 'axios';

export default function IntegrationApp(props) {
    let settings = {
        business_manager: {},
        ad_account: {},
        pixel: {},
        page: {},
        funding: {}
    };
    const link = props.current_shop.dashboard;
    const redirect = props.redirect;
    const [selected, setSelected] = useState(0);
    const [continues, setContinues] = useState(false);
    const [next, setNext] = useState(false);
    const [back, setBack] = useState(false);
    const [selectedSettings, setSelectedSettings] = useState(settings);
    const checkSettings = useCallback(
        (name) => {
            if (selected === 0) {
                setBack(false);
            } else {
                setBack(true);
            }
            if (!selectedSettings[name].value) {
                setNext(false);
            }
            else {
                if (selected === (tabs.length - 1)) {
                    setNext(false);
                } else {
                    setNext(true);
                }
            }

            if (selectedSettings.business_manager.value && selectedSettings.ad_account.value && selectedSettings.page.value && selectedSettings.pixel.value) {
                if (selected === (tabs.length - 1)) {
                    setContinues(true);
                } else {
                    setContinues(false);
                }
            }
            else {
                setContinues(false);
            }
        },
        [
            selected,
            selectedSettings,
            setContinues,
            setNext
        ]
    );

    const setSettings = useCallback(
        (
            name,
            val
        ) => {
            if (selectedSettings[name]) {
                selectedSettings[name] = val;
                setSelectedSettings(selectedSettings);
                checkSettings(name);
            }
        },
        [
            selectedSettings,
            setSelectedSettings,
            checkSettings
        ]
    );

    const choiceBusinessManager = [
        {
            label: 'Use an existing Business Manager',
            value: 'existing'
        },
        // {
        //     label: 'Create a new Business Manager',
        //     value: 'create'
        // }
    ];
    const choiceAccounts = [
        {
            label: 'Use an existing account',
            value: 'existing'
        },
        // {
        //     label: 'Create a new account',
        //     value: 'create'
        // }
    ];
    const choicePages = [
        {
            label: 'Use an existing Page',
            value: 'existing'
        },
        // {
        //     label: 'Create a new Page',
        //     value: 'create'
        // }
    ];
    const choicePixels = [
        {
            label: 'Use an existing Pixel',
            value: 'existing'
        },
        {
            label: 'Create a new Pixel',
            value: 'create'
        }
    ];

    const choiceFunding = [
        {
            label: 'Use an existing Payment Method',
            value: 'existing'
        },
        {
            label: 'Create a new Payment Method',
            value: 'create'
        }
    ];

    const handleTabChange = useCallback(
        (selectedTabIndex) => setSelected(selectedTabIndex),
        []
    );

    function existingOptions(selected) {
        let options = [];
        if (selected === 'business_manager') {
            (props.businesses || []).forEach(
                businesse => {
                    options.push({
                        label: businesse.label,
                        value: businesse.value
                    });
                }
            );
        }
        else if (selected === 'ad_account') {
            (props.businesses || []).forEach(
                businesse => {
                    (businesse.accounts || []).forEach(
                        account => {
                            if (selectedSettings.business_manager.value && selectedSettings.business_manager.value === businesse.value) {
                                options.push({
                                    label: account.label,
                                    value: account.value
                                });
                            }

                        }
                    );
                }
            );
        }
        else if (selected === 'page') {
            (props.businesses || []).forEach(
                businesse => {
                    (businesse.accounts || []).forEach(
                        account => {
                            (account.pages || []).forEach(
                                page => {
                                    if (selectedSettings.ad_account.value && selectedSettings.ad_account.value === account.value) {
                                        options.push({
                                            label: page.label,
                                            value: page.value
                                        });
                                    }
                                }
                            );
                        }
                    );
                }
            );
        }
        else if (selected === 'pixel') {
            (props.businesses || []).forEach(
                businesse => {
                    (businesse.accounts || []).forEach(
                        account => {
                            (account.pixels || []).forEach(
                                pixel => {
                                    if (selectedSettings.ad_account.value && selectedSettings.ad_account.value === account.value) {
                                        options.push({
                                            label: pixel.label,
                                            value: pixel.value
                                        });
                                    }
                                }
                            );
                        }
                    );
                }
            );
        }
        else if (selected === 'funding') {
            (props.businesses || []).forEach(
                businesse => {
                    (businesse.accounts || []).forEach(
                        account => {
                            (account.funding || []).forEach(
                                fund => {
                                    if (selectedSettings.ad_account.value && selectedSettings.ad_account.value === account.value) {
                                        options.push({
                                            label: fund.label,
                                            value: fund.value
                                        });
                                    }
                                }
                            );
                        }
                    );
                }
            );

        }
        return options;
    }

    function apiCreateData(selected) {
        let data = {
            url: '',
            params: function (label) {
                return {};
            }
        };
        if (selected === 'business_manager') {
            data.url = 'me/businesses';
            data.params = function (label) {
                return {
                    name: label,
                    vertical: 'ECOMMERCE'
                };
            };
        }
        else if (selected === 'ad_account' && selectedSettings.business_manager.value) {
            data.url = selectedSettings.business_manager.value + '/adaccount';
            data.params = function (label) {
                return {
                    name: label,
                    currency: 'USD',
                    timezone_id: 1,
                    end_advertiser: 'UNFOUND',
                    media_agency: 'UNFOUND',
                    partner: 'UNFOUND'
                };
            };
        }
        else if (selected === 'pixel') {
            data.url = 'act_' + selectedSettings.ad_account.value + '/adspixels';
            data.params = function (label) {
                return {name: label};
            };

        }
        else if (selected === 'page') {
            data.url = selectedSettings.business_manager.value + '/client_pages';
        }
        else if (selected === 'funding') {
            data.ad_account = selectedSettings.ad_account.value;
        }
        return data;
    }

    const save = useCallback(
        () => {
            axios.defaults.xsrfCookieName = 'csrftoken';
            axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
            axios.post('/shopify/fb_integration', {
                data: {
                    business_id: selectedSettings.business_manager.value,
                    account_id: selectedSettings.ad_account.value,
                    pixel: selectedSettings.pixel.value,
                    page: selectedSettings.page.value
                },
                token: props.token,
                user: props.user,
                shop: props.current_shop.domain
            }).then(function () {
                redirect.dispatch(Redirect.Action.APP, link);
            });
        },
        [selectedSettings]
    );

    const tabs = [
        {
            id: 'business_manager',
            content: '1. Select your Business Manager',
            text: 'Select a Facebook Business Manager you wish to use for advertising.',
            panelID: 'business_manager',
            childrens: (
                <Choicer choices={choiceBusinessManager}
                         options={existingOptions('business_manager')}
                         setings={selectedSettings.business_manager}
                         setSettings={setSettings}
                         createData={apiCreateData('business_manager')}
                         checkSettings={checkSettings}
                         type={'business_manager'}
                         error={"You don't have a Business Manager. Create an Business Manager on Facebook"}
                />
            )
        },
        {
            id: 'ad_account',
            content: '2. Select an Ad Account where you have the Admin role',
            text: 'Select an ad account you wish to use for advertising',
            panelID: 'ad_account',
            childrens: (
                <Choicer choices={choiceAccounts}
                         options={existingOptions('ad_account')}
                         setings={selectedSettings.ad_account}
                         setSettings={setSettings}
                         checkSettings={checkSettings}
                         createData={apiCreateData('ad_account')}
                         type={'ad_account'}
                         error={"You don't have a Ad Account. Create an Ad Account on Facebook"}
                />
            )
        },
        {
            id: 'pages',
            content: '3. Select Page',
            text: 'Select a Page to your account',
            panelID: 'page',
            childrens: (
                <Choicer choices={choicePages}
                         options={existingOptions('page')}
                         setings={selectedSettings.page}
                         setSettings={setSettings}
                         checkSettings={checkSettings}
                         createData={apiCreateData('page')}
                         type={'page'}
                         error={"You don't have aPage. Create an Page on Facebook"}
                />
            )
        },
        {
            id: 'pixels',
            content: '4. Select Pixel',
            text: 'Select a Pixel to your account',
            panelID: 'pixel',
            childrens: (
                <Choicer choices={choicePixels}
                         options={existingOptions('pixel')}
                         setings={selectedSettings.pixel}
                         setSettings={setSettings}
                         checkSettings={checkSettings}
                         createData={apiCreateData('pixel')}
                         type={'pixel'}
                />
            )
        },
        {
            id: 'payments',
            content: '5. Payment method',
            text: 'Add a Payment Method to your account',
            panelID: 'funding',
            childrens: (
                <ChoicerFunding
                    choices={choiceFunding}
                    options={existingOptions('funding')}
                    setings={selectedSettings.funding}
                    setSettings={setSettings}
                    checkSettings={checkSettings}
                    createData={apiCreateData('funding')}
                    type={'funding'}
                />
            )
        }
    ];
    return (
        <Page>
            <Layout>
                <Card
                    title='Connect Facebook'
                    secondaryFooterActions={[
                        {
                            content: 'CANCEL',
                            onAction: function () {
                                redirect.dispatch(Redirect.Action.APP, link);
                            }
                        }
                    ]}
                    primaryFooterAction={{
                        content: 'CONTINUE',
                        disabled: !continues,
                        onAction: save
                    }}
                >
                    <Card.Section>
                        <Tabs tabs={tabs} selected={selected} fitted>
                            <Card
                                title={tabs[selected].text}
                                secondaryFooterActions={[
                                    {
                                        content: 'BACK',
                                        disabled: !back,
                                        onAction: function () {
                                            handleTabChange(selected - 1);
                                        }

                                    }
                                ]}
                                primaryFooterAction={{
                                    content: 'NEXT',
                                    disabled: !next,
                                    primary: next,
                                    onAction: function () {
                                        handleTabChange(selected + 1)
                                    }
                                }}
                            >
                                <Card.Section>
                                    {tabs[selected].childrens}
                                </Card.Section>
                            </Card>
                        </Tabs>
                    </Card.Section>
                </Card>
            </Layout>
        </Page>
    );
}
