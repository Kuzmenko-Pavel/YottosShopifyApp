import React from "react";
import {Badge, Card, Layout, Link, List} from "@shopify/polaris";
import * as Redirect from "@shopify/app-bridge/actions/Navigation/Redirect";


export default function Options(props) {
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

    return (
        <Layout.AnnotatedSection
            title='You app options'>
            <Card sectioned title='You app options'
                  actions={props.current_shop.premium ? null : [
                      {
                          content: 'Upgrade to Premium Membership',
                          onAction: upgrade
                      }
                  ]}>
                <List type="bullet">
                    {props.current_shop.options.map(
                        function (
                            option,
                            index
                        ) {
                            let badge = [];
                            if (option.default) {
                                badge.push(<Badge key={'olibd' + index} progress="complete">default</Badge>);
                            }
                            if (option.premium && !option.active) {
                                badge.push(<Link key={'olibpl' + index} onClick={upgrade}>
                                        <Badge key={'olibp' + index} status="success" progress="incomplete">premium</Badge>
                                    </Link>
                                );
                                badge.push(<Link key={'olibl' + index}
                                                 onClick={upgrade}>Activated</Link>);
                            }
                            if (option.premium && option.active) {
                                badge.push(<Badge key={'olibpa' + index} status="success"
                                                  progress="complete">premium</Badge>);
                            }
                            return <List.Item key={'oli' + index} id={'oli' + index}>{option.label}{badge}</List.Item>;
                        }
                    )}
                </List>
            </Card>
        </Layout.AnnotatedSection>
    );
}