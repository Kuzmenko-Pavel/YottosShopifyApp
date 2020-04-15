import React, {useCallback, useState} from 'react';
import {Button, Form, FormLayout, TextField} from "@shopify/polaris";

export default function Create(props) {
    const data = props.createData;
    const [error, setError] = useState('');
    const [disabled, setDisabled] = useState(false);
    let textLabel = '';
    if (props.type === 'business_manager') {
        textLabel = 'Business Manager Name';
    }
    else if (props.type === 'ad_account') {
        textLabel = 'Ad Account Name';
    }
    else if (props.type === 'pixel') {
        textLabel = 'Pixel Name';
    }
    let defValue = '';
    if ((props.setings.existing || false) === false && props.setings.value) {
        defValue = props.setings.value;
        setDisabled(true);
    }


    const [label, setLabel] = useState(defValue);

    const handleSubmit = useCallback(
        (_event) => {
            if (data.url && label) {
                FB.api(data.url, 'post', data.params(label), function (response) {
                        if (response.error) {
                            setError(response.error.message);
                            setDisabled(false);
                        }
                        else {
                            props.setSettings({
                                label: label,
                                value: response.id,
                                existing: false
                            });
                            setDisabled(true);
                        }
                    }
                );
            }

        }, [
            label,
            setError,
            setDisabled
        ]
    );


    const handleLabelChange = useCallback((value) => {
        setLabel(value);
        setError('');
    }, []);
    return (<Form noValidate onSubmit={handleSubmit} preventDefault={true}>
        <FormLayout>
            <TextField
                value={label}
                onChange={handleLabelChange}
                label={textLabel}
                type="text"
                helpText={
                    <span>
                      We’ll use this name.
                    </span>
                }
                error={error}
                disabled={disabled}
            />

            <Button submit disabled={disabled}>Create</Button>
        </FormLayout>
    </Form>)
}