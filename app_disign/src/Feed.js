import React, {useCallback, useState} from "react";
import {Banner, Button, Card, Layout, Link, Stack} from "@shopify/polaris";


function FeedBanner(props) {
    let url = 'https://' + props.current_shop.domain + '/a/ytt_feed/' + props.current_shop.feed.link + '.xml';
    return (
        <Stack>
            <Banner>{props.current_shop.feed.sectioned_title} - {' '} <Link url={url}
                                                                            external={true}>{props.current_shop.feed.link + '.xml'}</Link></Banner>
            <Banner>{props.current_shop.feed.catalog_title} - {' '} <Link url={props.current_shop.feed.catalog_link}
                                                                          external={true}>{props.current_shop.feed.catalog_link}</Link></Banner>
        </Stack>
    );
}


export default function Feed(props) {
    const [active, setActive] = useState(false);
    const handleChange = useCallback(() => {
        if (!active) {
            window.ga('send', 'event', 'Generate', 'Feed', props.current_shop.feed.link);
            if (window.fbq) {
                fbq('trackCustom', 'Generate_Feed_' + props.current_shop.feed.link);
            }
            setActive(!active);
        }
    }, [active]);
    return (
        <Layout.AnnotatedSection
            title={props.current_shop.feed.title}
            description={props.current_shop.feed.description}>
            <Card sectioned title={props.current_shop.feed.sectioned_title}>
                <Stack spacing="loose" vertical>
                    {active ? <FeedBanner current_shop={props.current_shop}></FeedBanner> : null}
                    <Stack distribution="trailing">
                        <Button onClick={handleChange}>Generate Feed</Button>
                    </Stack>
                </Stack>
            </Card>
        </Layout.AnnotatedSection>
    );
}
