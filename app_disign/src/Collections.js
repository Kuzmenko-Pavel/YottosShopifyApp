import React, {useCallback, useState} from "react";
import axios from 'axios';
import {
    Badge,
    Button,
    Card,
    Checkbox,
    Heading,
    Layout,
    Link,
    List,
    Modal,
    Scrollable,
    Sheet,
    TextContainer
} from '@shopify/polaris';
import {Redirect} from '@shopify/app-bridge/actions';
import {MobileCancelMajorMonotone} from '@shopify/polaris-icons';


export default function Collections(props) {
    const premium = props.current_shop.premium;
    const [sheetActive, setSheetActive] = useState(false);
    const [active, setActive] = useState(false);
    const [salesChannels, setData] = useState(props.current_shop.collections);

    const handleChange = useCallback(() => setActive(!active), [active]);
    const toggleSheetOpen = useCallback(
        () => {
            window.ga('send', 'event', 'Click', 'Open', 'Collections');
            if (window.fbq) {
                fbq('trackCustom', 'Open_Collections');
            }
            setSheetActive((sheetActive) => !sheetActive);
        },
        []
    );

    function toggleSheetClose() {
        toggleSheetOpen();
        salesChannels.map((channel) => {
            setData(salesChannels.map(
                object => {
                    if (channel && object.label === channel.label && object.oldValue !== undefined) {
                        object.value = object.oldValue;
                        delete object.oldValue;
                        return object;
                    }
                    return object;
                }));
        });
    }

    function toggleSheetSave() {
        if (premium) {
            toggleSheetOpen();
            salesChannels.map((channel) => {
                setData(salesChannels.map(
                    object => {
                        if (channel && object.label === channel.label) {
                            delete object.oldValue;
                            return object;
                        }
                        return object;
                    }));
            });
            axios.defaults.xsrfCookieName = 'csrftoken';
            axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
            axios.post('/shopify/save?type=collections', {
                feed_name: props.current_shop.feed_name,
                data: salesChannels,
                shop: props.current_shop.domain
            });
        }
        else {
            toggleSheetClose();
            handleChange();
        }
    }

    function upgrade() {
        window.ga('send', 'event', 'Order', 'Upgrade', 'Collections');
        window.ga('ec:addProduct', {
            'id': '1',
            'name': 'Premium',
            'price': '29.00',
            'variant': 'Collections',
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
                content_category: 'Collections',
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

    var description = <div>
        <p>When you generate a feed, build collections that will be in your product feed.</p>
        <p>For this, be guided by your strategy:</p>
        <p><Link url='https://feed-product.com/help_center/strategies_in_feed_product.html#step-2' external={true}>-
            attract new thematic audience</Link></p>
        <p><Link url='https://feed-product.com/help_center/strategies_in_feed_product.html#step-3' external={true}>-
            dynamic remarketing</Link></p>
        <p><Link url='https://feed-product.com/help_center/strategies_in_feed_product.html#step-4' external={true}>-
            discounts to increase loyalty</Link></p>
    </div>;
    return (
        <Layout.AnnotatedSection
            title='Your collections'
            description={description}>
            <Card sectioned subdued title='Collections uploaded to your feed'>
                <div
                    style={{
                        alignItems: 'center',
                        display: 'flex',
                        justifyContent: 'space-between',
                        width: '100%'
                    }}
                >
                    <List>
                        {salesChannels.map(
                            (
                                channel,
                                index
                            ) => {
                                var badge = <Badge key={'olibpa' + index} status="default"
                                                   progress="incomplete">premium</Badge>;
                                if (channel.value) {
                                    badge =
                                        <Badge key={'olibpa' + index} status="success" progress="complete">on</Badge>;
                                }
                                else {
                                    if (premium) {
                                        badge = <Badge key={'olibpa' + index} status="success"
                                                       progress="incomplete">off</Badge>;
                                    }
                                }
                                return <List.Item key={index}>{channel.label}{badge}</List.Item>;
                            }
                        )}
                    </List>
                    <Button onClick={toggleSheetOpen}>Manage collections</Button>
                </div>
            </Card>
            <Sheet open={sheetActive} onClose={toggleSheetClose}>
                <div
                    style={{
                        display: 'flex',
                        flexDirection: 'column',
                        height: '100%'
                    }}
                >
                    <div
                        style={{
                            alignItems: 'center',
                            borderBottom: '1px solid #DFE3E8',
                            display: 'flex',
                            justifyContent: 'space-between',
                            padding: '1.6rem',
                            width: '100%'
                        }}
                    >
                        <Heading>Manage collections</Heading>
                        <Button
                            accessibilityLabel="Cancel"
                            icon={MobileCancelMajorMonotone}
                            onClick={toggleSheetClose}
                            plain
                        />
                    </div>
                    <Scrollable style={{
                        padding: '1.6rem',
                        height: '100%'
                    }}>
                        <List type="bullet">
                            {salesChannels.map(function (
                                channel,
                                index
                            ) {
                                return <List.Item key={index + 1} id={index + 1}>
                                    <Checkbox
                                        key={index + 1}
                                        label={channel.label}
                                        checked={channel.value}
                                        onChange={(v) => {
                                            setData(salesChannels.map(
                                                object => {
                                                    if (object.label === channel.label) {
                                                        var oldValue = channel.value;
                                                        if (channel.oldValue !== undefined) {
                                                            oldValue = channel.oldValue;
                                                        }
                                                        return {
                                                            ...object,
                                                            oldValue: oldValue,
                                                            value: v
                                                        }
                                                    }
                                                    else return object;
                                                }))
                                        }}
                                    />
                                </List.Item>;
                            })}
                        </List>
                    </Scrollable>
                    <div
                        style={{
                            alignItems: 'center',
                            borderTop: '1px solid #DFE3E8',
                            display: 'flex',
                            justifyContent: 'space-between',
                            padding: '1.6rem',
                            width: '100%'
                        }}
                    >
                        <Button onClick={toggleSheetClose}>Cancel</Button>
                        <Button primary onClick={toggleSheetSave}>
                            Save
                        </Button>
                    </div>
                </div>
            </Sheet>
            <Modal
                open={active}
                onClose={handleChange}
                title="Upgrade to Premium Membershi"
                primaryAction={{
                    content: 'Upgrade to Premium Membership',
                    onAction: upgrade
                }}
                secondaryActions={[
                    {
                        content: 'Close',
                        onAction: handleChange
                    }
                ]}
            >
                <Modal.Section>
                    <TextContainer>
                        <p>
                            This option is available only in premium.
                        </p>
                    </TextContainer>
                </Modal.Section>
            </Modal>
        </Layout.AnnotatedSection>
    );
}
