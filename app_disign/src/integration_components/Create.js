import React, {useCallback, useState} from 'react';
import {Button, Form, FormLayout, TextField} from "@shopify/polaris";

export default function Create(props) {
    const data = props.createData;
    let defValue = '';
    if ((props.setings.existing || false) === false) {
        defValue = props.setings.value || '';
    }
    console.log(props.setings);
    const [error, setError] = useState('');
    const [label, setLabel] = useState(defValue);

    const handleSubmit = useCallback(
        (_event) => {
            console.log(label);
            if (data.url && label) {
                FB.api(data.url, 'post', data.params(label), function (response) {
                        if (response.error) {
                            setError(response.error.message);
                        }
                        else {
                            console.log(response);
                            props.setSettings({
                                label: label,
                                value: response.id,
                                existing: false
                            });
                        }
                    }
                );
            }

        }, [
            label,
            setError
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
                label="Business Manager Name"
                type="text"
                helpText={
                    <span>
                      We’ll use this name.
                    </span>
                }
                error={error}
                disabled={(defValue != '') ? true : false}
            />

            <Button submit disabled={(defValue != '') ? true : false}>Create</Button>
        </FormLayout>
    </Form>)
}