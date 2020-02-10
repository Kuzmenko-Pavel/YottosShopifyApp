import React, {useCallback, useState} from "react";
import {Banner, Button, Card, Layout, Link, Stack} from "@shopify/polaris";


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
    let url = 'https://' + props.current_shop.domain + '/a/ytt_feed/' + props.current_shop.feed.link + '.xml';
    return (
        <Layout.AnnotatedSection
            title={props.current_shop.feed.title}
            description={props.current_shop.feed.description}>
            <Card sectioned title={props.current_shop.feed.sectioned_title}>
                <Stack spacing="loose" vertical>
                    {active ? <Banner>{props.current_shop.feed.sectioned_title} - {' '} <Link url={url}
                                                                                              external={true}>{props.current_shop.feed.link + '.xml'}</Link>
                    </Banner> : null}
                    <Stack distribution="trailing">
                        <Button onClick={handleChange}>Generate Feed</Button>
                    </Stack>
                </Stack>
            </Card>
        </Layout.AnnotatedSection>
    );
}
