import React, {useCallback, useState} from "react";
import {Button, Card, Heading, Layout, Modal, Scrollable, Sheet, TextContainer} from "@shopify/polaris";
import * as Redirect from "@shopify/app-bridge/actions/Navigation/Redirect";
import {MobileCancelMajorMonotone} from "@shopify/polaris-icons";
import Geo from "./Geo";


export default function Integrtion(props) {
    const geoOptions = Array.from(Array(100)).map((
        _,
        index
    ) => ({
        value: `country ${index}`,
        label: `Country ${index}`
    }));
    const [selectedOptionsGeo, setSelectedOptionsGeo] = useState([]);
    const relevant_geoOptions = Array.from(Array(100)).map((
        _,
        index
    ) => ({
        value: `country ${index}`,
        label: `Country ${index}`
    }));
    const [selectedOptionsGeoRel, setSelectedOptionsGeoRel] = useState([]);
    const retargeting_geoOptions = Array.from(Array(100)).map((
        _,
        index
    ) => ({
        value: `country ${index}`,
        label: `Country ${index}`
    }));
    const [selectedOptionsGeoRet, setSelectedOptionsGeoRet] = useState([]);
    const premium = props.current_shop.premium;
    const liStyle = {
        fontSize: '30px',
        marginBottom: '10px'
    };
    const divStyle = {
        position: 'relative',
        top: '-5px'
    };

    const [sheetActive, setSheetActive] = useState(false);
    const toggleSheetOpen = useCallback(
        () => {
            if (premium) {
                window.ga('send', 'event', 'Click', 'Open', 'NewAuditory');
                if (window.fbq) {
                    fbq('trackCustom', 'Open_NewAuditory');
                }
                setSheetActive((sheetActive) => !sheetActive);
            } else {
                handleChange();
            }
        },
        []
    );

    function toggleSheetClose() {
        toggleSheetOpen();
    }

    function toggleSheetSave() {
        if (premium) {
            toggleSheetOpen();
        }
        else {
            toggleSheetClose();
            handleChange();
        }
    }


    const [relevant_sheetActive, relevant_setSheetActive] = useState(false);
    const relevant_toggleSheetOpen = useCallback(
        () => {
            if (premium) {
                window.ga('send', 'event', 'Click', 'Open', 'Relevant');
                if (window.fbq) {
                    fbq('trackCustom', 'Open_Relevant');
                }
                relevant_setSheetActive((relevant_sheetActive) => !relevant_sheetActive);
            } else {
                handleChange();
            }
        },
        []
    );

    function relevant_toggleSheetClose() {
        relevant_toggleSheetOpen();
    }

    function relevant_toggleSheetSave() {
        if (premium) {
            relevant_toggleSheetOpen();
        }
        else {
            relevant_toggleSheetClose();
            handleChange();
        }
    }

    const [retargeting_sheetActive, retargeting_setSheetActive] = useState(false);
    const retargeting_toggleSheetOpen = useCallback(
        () => {
            if (premium) {
                window.ga('send', 'event', 'Click', 'Open', 'Relevant');
                if (window.fbq) {
                    fbq('trackCustom', 'Open_Relevant');
                }
                retargeting_setSheetActive((relevant_sheetActive) => !relevant_sheetActive);
            } else {
                handleChange();
            }
        },
        []
    );

    function retargeting_toggleSheetClose() {
        retargeting_toggleSheetOpen();
    }

    function retargeting_toggleSheetSave() {
        if (premium) {
            retargeting_toggleSheetOpen();
        }
        else {
            retargeting_toggleSheetClose();
            handleChange();
        }
    }


    const [active, setActive] = useState(false);
    const handleChange = useCallback(() => setActive(!active), [active]);

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

    function testAPI() {
        console.log('Welcome!  Fetching your information.... ');
        FB.api('/me', function (response) {
            console.log('Successful login for: ' + response.name);
            console.log(response);
        });
    }

    function statusChangeCallback(response) {
        console.log('statusChangeCallback');
        console.log(response);
        if (response.status === 'connected') {
            testAPI();
        } else {
            FB.login(
                statusChangeCallback, {
                    scope: 'email,ads_management,ads_read,read_insights,business_management,catalog_management,manage_pages',
                    auth_type: 'rerequest'
                }
            );
            console.log('Not Login');
        }
    }

    function connectFb() {
        FB.getLoginStatus(function (response) {   // See the onlogin handler
            statusChangeCallback(response);
        });
    }

    if (props.current_shop.feed.integration) {
        if (props.current_shop.feed.integration.complite) {
            return (
                <Layout.AnnotatedSection
                    title={props.current_shop.feed.integration.text.title}
                    description={props.current_shop.feed.integration.text.description}>
                    <Card sectioned title={props.current_shop.feed.integration.text.sectioned_title}>
                        <ol>
                            <li style={liStyle}>
                                <div style={divStyle}>
                                    <Button external={true} fullWidth={true} primary={true}
                                            onClick={toggleSheetOpen}>
                                        {props.current_shop.feed.integration.text.buttons.new_auditory}
                                    </Button>
                                </div>
                            </li>
                            <li style={liStyle}>
                                <div style={divStyle}>
                                    <Button external={true} fullWidth={true} primary={true}
                                            onClick={retargeting_toggleSheetOpen}>
                                        {props.current_shop.feed.integration.text.buttons.retargeting}
                                    </Button>
                                </div>
                            </li>
                            <li style={liStyle}>
                                <div style={divStyle}>
                                    <Button external={true} fullWidth={true} primary={true}
                                            onClick={relevant_toggleSheetOpen}>
                                        {props.current_shop.feed.integration.text.buttons.relevant}
                                    </Button>
                                </div>
                            </li>
                        </ol>
                    </Card>
                    <Sheet open={sheetActive}>
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
                                <Heading>{props.current_shop.feed.integration.text.sheet.new_auditory.heading}</Heading>
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
                                <Geo geo={geoOptions}
                                     selectedOptions={selectedOptionsGeo}
                                     setSelectedOptions={setSelectedOptionsGeo}></Geo>
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
                                <Button onClick={toggleSheetClose}>
                                    {props.current_shop.feed.integration.text.sheet.new_auditory.cancel}
                                </Button>
                                <Button primary onClick={toggleSheetSave}>
                                    {props.current_shop.feed.integration.text.sheet.new_auditory.save}
                                </Button>
                            </div>
                        </div>
                    </Sheet>

                    <Sheet open={retargeting_sheetActive}>
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
                                <Heading>{props.current_shop.feed.integration.text.sheet.retargeting.heading}</Heading>
                                <Button
                                    accessibilityLabel="Cancel"
                                    icon={MobileCancelMajorMonotone}
                                    onClick={retargeting_toggleSheetClose}
                                    plain
                                />
                            </div>
                            <Scrollable style={{
                                padding: '1.6rem',
                                height: '100%'
                            }}>
                                <Geo geo={retargeting_geoOptions}
                                     selectedOptions={selectedOptionsGeoRet}
                                     setSelectedOptions={setSelectedOptionsGeoRet}></Geo>
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
                                <Button onClick={retargeting_toggleSheetClose}>
                                    {props.current_shop.feed.integration.text.sheet.retargeting.cancel}
                                </Button>
                                <Button primary onClick={retargeting_toggleSheetSave}>
                                    {props.current_shop.feed.integration.text.sheet.retargeting.save}
                                </Button>
                            </div>
                        </div>
                    </Sheet>

                    <Sheet open={relevant_sheetActive}>
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
                                <Heading>{props.current_shop.feed.integration.text.sheet.relevant.heading}</Heading>
                                <Button
                                    accessibilityLabel="Cancel"
                                    icon={MobileCancelMajorMonotone}
                                    onClick={relevant_toggleSheetClose}
                                    plain
                                />
                            </div>
                            <Scrollable style={{
                                padding: '1.6rem',
                                height: '100%'
                            }}>
                                <Geo geo={relevant_geoOptions}
                                     selectedOptions={selectedOptionsGeoRel}
                                     setSelectedOptions={setSelectedOptionsGeoRel}></Geo>
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
                                <Button onClick={relevant_toggleSheetClose}>
                                    {props.current_shop.feed.integration.text.sheet.relevant.cancel}
                                </Button>
                                <Button primary onClick={relevant_toggleSheetSave}>
                                    {props.current_shop.feed.integration.text.sheet.relevant.save}
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
            )
        }
        else {
            return (
                <Layout.AnnotatedSection
                    title={props.current_shop.feed.integration.text.title}
                    description={props.current_shop.feed.integration.text.description}>
                    <Card sectioned title={props.current_shop.feed.integration.text.sectioned_title}>
                        <Button external={true} fullWidth={true} primary={true} onClick={connectFb}>
                            {props.current_shop.feed.integration.text.buttons.activate}
                        </Button>
                    </Card>
                </Layout.AnnotatedSection>
            )
        }
    }
    return (null);
}
