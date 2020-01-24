import React, {Component} from "react";
import {Badge, Card, Layout, Link, List} from "@shopify/polaris";

class ListItem extends Component {
    render() {
        let badge = [];
        if (this.props.option.default) {
            badge.push(<Badge progress="complete" >default</Badge>);
        }
        if (this.props.option.premium && !this.props.option.active) {
            badge.push(<Link url="https://help.shopify.com/manual">
                    <Badge status="success" progress="incomplete">premium</Badge>
                </Link>
            );
            badge.push(<Link url="https://help.shopify.com/manual">Activated</Link>);
        }
        if (this.props.option.premium && this.props.option.active) {
            badge.push(<Link url="https://help.shopify.com/manual">
                    <Badge status="success" progress="complete">premium</Badge>
                </Link>
            );
        }
        return (
            <List.Item key={this.props.index}>{this.props.option.label}
                {badge}
            </List.Item>
        );
    }
}

class Options extends Component {
    render() {
        return (
            <Layout.AnnotatedSection
                title='You app options'>
                <Card sectioned title='You app options'
                      actions={[{content: 'Upgrade to Premium Membership'}]}>
                    <List type="bullet">
                        {this.props.current_shop.options.map((
                            option,
                            index
                        ) => <ListItem key={index} index={index} option={option || {}}></ListItem>)}
                    </List>
                </Card>
            </Layout.AnnotatedSection>
        );
    }
}

export default Options;