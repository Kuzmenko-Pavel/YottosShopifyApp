import React, {useCallback, useState} from "react";
import {
    Button,
    Card,
    Heading,
    Layout,
    List,
    Modal,
    Scrollable,
    Sheet,
    TextContainer,
    TextField
} from '@shopify/polaris';
import {MobileCancelMajorMonotone} from '@shopify/polaris-icons';


export default function UTM(props) {
    const premium = props.current_shop.premium;
    const [sheetActive, setSheetActive] = useState(false);
    const [active, setActive] = useState(false);
    const [salesChannels, setData] = useState(props.current_shop.utm);

    const handleChange = useCallback(() => setActive(!active), [active]);
    const toggleSheetOpen = useCallback(
        () => {
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
        }
        else {
            toggleSheetClose();
            handleChange();
        }
    }

    return (
        <Layout.AnnotatedSection
            title='You UTM tag'>
            <Card sectioned subdued title='UTM tag'>
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
                            ) => (<List.Item key={index}>{channel.label} : {channel.value}</List.Item>)
                        )}
                    </List>
                    <Button onClick={toggleSheetOpen}>Manage utm tags</Button>
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
                        <Heading>Manage utm tags</Heading>
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
                                    <TextField key={index + 1} id={index + 1} label={channel.label}
                                               value={channel.value} onChange={(v) => {
                                        setData(salesChannels.map(
                                            object => {
                                                if (object.label === channel.label) {
                                                    return {
                                                        ...object,
                                                        oldValue: channel.oldValue || channel.value,
                                                        value: v
                                                    }
                                                }
                                                else return object;
                                            }))
                                    }}/>
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
                    onAction: handleChange
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
                            Эта опуия доступна только в премиум.
                        </p>
                    </TextContainer>
                </Modal.Section>
            </Modal>
        </Layout.AnnotatedSection>
    );
}
