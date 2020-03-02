import React, {useCallback, useEffect, useState} from 'react';
import {Badge, Layout, Link, List, Modal, Page, Stack, TextContainer} from '@shopify/polaris';
import Feed from './Feed';
import Options from './Options';
import UTM from './Utm';
import Collections from './Collections';
import * as Redirect from "@shopify/app-bridge/actions/Navigation/Redirect";

export default function App(props) {
    const premium = window.current_shop.premium;
    const [active, setActive] = useState(false);
    const handleChange = useCallback(() => {
        setActive(!active);
    }, [active]);

    function upgrade() {
        window.ga('send', 'event', 'Order', 'Upgrade', 'Options');
        window.ga('ec:addProduct', {
            'id': '1',
            'name': 'Premium',
            'price': '29.00',
            'variant': 'Options',
            'quantity': 1
        });
        window.ga('ec:setAction', 'checkout', {
            'step': 1,
            'id': window.t
        });
        if (window.fbq) {
            fbq('track', 'InitiateCheckout', {
                content_ids: [1],
                content_name: 'Premium',
                content_type: 'product',
                content_category: 'Options',
                contents: [
                    {
                        'id': '1',
                        'quantity': 1
                    }
                ],
                currency: "USD",
                value: 29.00
            });
        }
        props.redirect.dispatch(Redirect.Action.APP, props.current_shop.billing);
    }

    useEffect(
        () => {
            if (!premium) {
                let timer1 = setTimeout(() => setActive(true), 5000);
                return () => {
                    clearTimeout(timer1);
                };
            }
        },
        []
    );
    const h3Style = {textAlign: 'center'};
    const title = <div style={h3Style} className="Polaris-Heading">Activate 60 day PREMIUM PLAN for free!</div>;
    return (
        <Page>
            <Layout>
                <Feed current_shop={window.current_shop} redirect={props.redirect} />
                <Collections current_shop={window.current_shop} redirect={props.redirect} />
                <UTM current_shop={window.current_shop} redirect={props.redirect} />
                <Options current_shop={window.current_shop} redirect={props.redirect}/>
                <Modal
                    open={active}
                    onClose={handleChange}
                    title={title}
                    primaryAction={{
                        content: 'Activate Premium plan',
                        onAction: upgrade
                    }}
                >
                    <Modal.Section>
                        <Stack vertical>
                            <Stack.Item>
                                <TextContainer>
                                    <p>
                                        You can activate a premium account and get additional features.
                                    </p>
                                    <List type="bullet">
                                        {window.current_shop.options.map(
                                            function (
                                                option,
                                                index
                                            ) {
                                                if (option.premium && !option.active) {
                                                    let badge = [];
                                                    badge.push(<Link key={'olibpl' + index} onClick={upgrade}>
                                                            <Badge key={'olibp' + index} status="success"
                                                                   progress="incomplete">premium</Badge>
                                                        </Link>
                                                    );
                                                    badge.push(<Link key={'olibl' + index}
                                                                     onClick={upgrade}>Activate Premium plan</Link>);
                                                    return <List.Item key={'oli' + index}
                                                                      id={'oli' + index}>{option.label}{badge}</List.Item>;
                                                }
                                            }
                                        )}
                                    </List>
                                </TextContainer>
                            </Stack.Item>
                            <Stack.Item fill>

                            </Stack.Item>
                        </Stack>
                    </Modal.Section>
                </Modal>
            </Layout>
        </Page>
    );
}
