import React, { Component } from "react";
import {Card, Layout, TextField} from "@shopify/polaris";

class Feed extends Component {
    render() {
        let url = 'https://' + this.props.current_shop.domain + '/a/ytt_feed/' + this.props.current_shop.feed.link + '.xml';
            return (
                <Layout.AnnotatedSection
                    title={this.props.current_shop.feed.title}
                    description={this.props.current_shop.feed.description}>
                    <Card sectioned title={this.props.current_shop.feed.sectioned_title} actions={[{content: 'Copy to clipboard'}]}>
                        <TextField type="text" labelHidden value={url} disabled/>
                    </Card>
                </Layout.AnnotatedSection>
            );
    }
}

export default Feed;