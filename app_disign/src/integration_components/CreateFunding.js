import React, {useCallback, useState} from 'react';
import {Button} from "@shopify/polaris";

export default function CreateFunding(props) {
    const data = props.createData;
    const [error, setError] = useState('');
    const [disabled, setDisabled] = useState(false);
    if ((props.setings.existing || false) === false && props.setings.value) {
        setDisabled(true);
    }
    else if (props.setings.existing === true && props.setings.value) {
        props.setSettings(props.type, {});
    }
    else {
        props.checkSettings(props.type);
    }
    const handleSubmit = useCallback(
        (_event) => {
            FB.ui({
                account_id: data.ad_account,
                display: 'popup',
                method: 'ads_payment'
            }, function (response) {
                console.log(response);
                if (response) {
                    FB.api('/act_' + data.ad_account + '/?fields=funding_source_details', function (response) {
                        if (response && response.funding_source_details) {
                            setDisabled(true);
                            props.setSettings(props.type, {
                                label: response.funding_source_details.display_string,
                                value: response.funding_source_details.id,
                                existing: false
                            });
                        }
                        else {
                            setDisabled(false);
                        }

                    });
                } else {
                    setDisabled(false);
                }
            });
        }, [
            setError,
            setDisabled
        ]
    );
    return (
        <Button onClick={handleSubmit} disabled={disabled}>Create</Button>
    )
}