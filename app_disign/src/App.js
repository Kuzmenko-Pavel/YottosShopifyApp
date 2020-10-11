import React, {useCallback, useEffect, useState} from 'react';
import YouTube from 'react-youtube';
import cookie from 'react-cookies';
import {Badge, Layout, Link, List, Modal, Page, Stack, TextContainer} from '@shopify/polaris';
import Feed from './Feed';
import Options from './Options';
import UTM from './Utm';
import Collections from './Collections';
import Integrtion from './Integration';
import * as Redirect from "@shopify/app-bridge/actions/Navigation/Redirect";
import * as Button from "@shopify/app-bridge/actions/Button";

export default function App(props) {
    const watchVideo = cookie.load('watchVideo');
    const expiresVideo = new Date();
    const maxAgeVideo = 60 * 60 * 24 * 365;
    expiresVideo.setDate(Date.now() + 1000 * maxAgeVideo);
    const watchPromo = cookie.load('watchPromo');
    const expiresPromo = new Date();
    const maxAgePromo = 60 * 60 * 12;
    expiresPromo.setDate(Date.now() + 1000 * maxAgePromo);
    const premium = props.current_shop.premium;
    const [active, setActive] = useState(false);
    const [activeYoutube, setActiveYoutube] = useState(false);
    const handleChange = useCallback(() => {
        setActive(!active);
    }, [active]);
    const handleChangeYoutube = useCallback(() => {
        setActiveYoutube(!activeYoutube);
    }, [
        activeYoutube,
        props
    ]);
    if (props.buttons.help) {
        props.buttons.help.subscribe(Button.Action.CLICK, function () {
            setActiveYoutube(true);
        });
    }

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
            if (!watchVideo) {
                setActiveYoutube(true);
                cookie.save('watchVideo', true, {
                    path: '/',
                    Expires: expiresVideo,
                    secure: true,
                    maxAge: maxAgeVideo
                });
            }
            else {
                if (!premium) {
                    if (!watchPromo) {
                        let timer1 = setTimeout(() => {
                            setActive(true);
                            cookie.save('watchPromo', true, {
                                path: '/',
                                Expires: expiresPromo,
                                secure: true,
                                maxAge: maxAgePromo
                            });
                        }, 8000);
                        return () => {
                            clearTimeout(timer1);
                        };
                    }
                }
            }
        },
        []
    );
    const h3Style = {textAlign: 'center'};
    const title = <div style={h3Style} className="Polaris-Heading">Activate 60 day PREMIUM PLAN for free!</div>;
    const youtube_opts = {
        height: '500px',
        width: '100%',
        playerVars: {
            // https://developers.google.com/youtube/player_parameters
            autoplay: 0,
            color: 'red',
            enablejsapi: 1,
            loop: 1,
            rel: 0
        }
    };

    function _onReady(event) {
        event.target.pauseVideo();
    }

    return (
        <Page>
            <Layout>
                <Feed current_shop={props.current_shop} redirect={props.redirect}/>
                <Integrtion current_shop={props.current_shop} redirect={props.redirect}/>
                <Collections current_shop={props.current_shop} redirect={props.redirect}/>
                <UTM current_shop={props.current_shop} redirect={props.redirect}/>
                <Options current_shop={props.current_shop} redirect={props.redirect}/>
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
                                        {props.current_shop.options.map(
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
                <Modal
                    large
                    title={'HOW TO CONFIGURE FEED PRODUCT IN SHOPIFY'}
                    open={activeYoutube}
                    onClose={handleChangeYoutube}
                >
                    <Modal.Section>
                        <Stack vertical>
                            <Stack.Item>
                                <YouTube videoId="A9-Rt6yXad8" opts={youtube_opts} onReady={_onReady}/>
                            </Stack.Item>
                        </Stack>
                    </Modal.Section>
                </Modal>
            </Layout>
        </Page>
    );
}
