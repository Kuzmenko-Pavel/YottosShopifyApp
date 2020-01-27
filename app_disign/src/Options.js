import React, {Component} from "react";
import {Badge, Card, Layout, Link, List} from "@shopify/polaris";


class Options extends Component {
    render() {
        return (
            <Layout.AnnotatedSection
                title='You app options'>
                <Card sectioned title='You app options'
                      actions={[{content: 'Upgrade to Premium Membership'}]}>
                    <List type="bullet">
                        {this.props.current_shop.options.map(
                            function (option,
                            index) {
                                let badge = [];
                                if (option.default) {
                                    badge.push(<Badge key={ 'olibd' + index } progress="complete" >default</Badge>);
                                }
                                if (option.premium && !option.active) {
                                    badge.push(<Link key={ 'olibpl' + index } url="https://help.shopify.com/manual">
                                            <Badge key={ 'olibp' + index } status="success" progress="incomplete">premium</Badge>
                                        </Link>
                                    );
                                    badge.push(<Link key={ 'olibl' + index } url="https://help.shopify.com/manual">Activated</Link>);
                                }
                                if (option.premium && option.active) {
                                    badge.push(<Link key={ 'olibpla' + index } url="https://help.shopify.com/manual">
                                            <Badge key={ 'olibpa' + index } status="success" progress="complete">premium</Badge>
                                        </Link>
                                    );
                                }
                                return <List.Item key={ 'oli' + index } id={ 'oli' +  index}>{option.label}{badge}</List.Item>;
                            }
                        )}
                    </List>
                </Card>
            </Layout.AnnotatedSection>
        );
    }
}

export default Options;