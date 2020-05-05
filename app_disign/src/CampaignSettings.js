import React from 'react';
import {Button, Heading, Scrollable, Sheet} from '@shopify/polaris';
import {MobileCancelMajorMonotone} from "@shopify/polaris-icons";
import RunToggleCampaign from "./RunCampaign";
import CampaignBudget from "./CampaignBudget";
import Geo from "./Geo";

export default function CampaignSettings(props) {
    return (
        <Sheet open={props.sheetActive}>
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
                        onClick={props.toggleSheetClose}
                        plain
                    />
                </div>
                <Scrollable style={{
                    padding: '1.6rem',
                    height: '100%'
                }}>
                    <RunToggleCampaign
                        campaignRun={props.campaignRun}
                        setCampaignRun={props.setCampaignRun}
                    ></RunToggleCampaign>
                    <CampaignBudget
                        budgetValue={props.budgetValue}
                        setBudget={props.setBudget}
                    ></CampaignBudget>
                    <Geo geo={props.geoOptions}
                         selectedOptions={props.selectedOptionsGeo}
                         setSelectedOptions={props.setSelectedOptionsGeo}></Geo>

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
                    <Button onClick={props.toggleSheetClose}>
                        {props.current_shop.feed.integration.text.sheet.new_auditory.cancel}
                    </Button>
                    <Button primary onClick={props.toggleSheetSave}>
                        {props.current_shop.feed.integration.text.sheet.new_auditory.save}
                    </Button>
                </div>
            </div>
        </Sheet>
    );
}