import React, {useCallback} from 'react';
import {SettingToggle, TextField} from '@shopify/polaris';

export default function CampaignBudget(props) {
    const handleTextFieldChange = useCallback(
        (value) => props.setBudget(value),
        [props]
    );
    return (
        <SettingToggle
        >
            <TextField
                label="Daily Budget"
                type="number"
                value={props.budgetValue}
                onChange={handleTextFieldChange}
                prefix="$"
                min="50.00"
            />
        </SettingToggle>
    );
}