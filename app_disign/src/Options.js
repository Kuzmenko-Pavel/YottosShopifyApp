import React from "react";
import {Badge, Card, Layout, Link, List} from "@shopify/polaris";
import * as Redirect from "@shopify/app-bridge/actions/Navigation/Redirect";


export default function Options(props) {
    function upgrade() {
        props.redirect.dispatch(Redirect.Action.APP, props.current_shop.billing);
    }

    return (
        <Layout.AnnotatedSection
            title='You app options'>
            <Card sectioned title='You app options'
                  actions={[
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
                                badge.push(<Link key={'olibpla' + index} onClick={upgrade}>
                                        <Badge key={'olibpa' + index} status="success" progress="complete">premium</Badge>
                                    </Link>
                                );
                            }
                            return <List.Item key={'oli' + index} id={'oli' + index}>{option.label}{badge}</List.Item>;
                        }
                    )}
                </List>
            </Card>
        </Layout.AnnotatedSection>
    );
}