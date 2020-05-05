import React, {useCallback} from 'react';
import {SettingToggle, TextStyle} from '@shopify/polaris';

export default function RunToggleCampaign(props) {

    const handleToggle = useCallback(() => props.setCampaignRun((active) => !active), []);

    const contentStatus = props.campaignRun ? 'Stop' : 'Run';
    const textStatus = props.campaignRun ? 'starting' : 'stopping';

    return (
        <SettingToggle
            action={{
                content: contentStatus,
                onAction: handleToggle
            }}
            enabled={props.campaignRun}
        >
            This campaign is <TextStyle variation="strong">{textStatus}</TextStyle>.
        </SettingToggle>
    );
}