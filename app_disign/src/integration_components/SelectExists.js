import React, {useCallback, useState} from 'react';
import {Select} from "@shopify/polaris";

export default function SelectExists(props) {
    console.log('SelectExists', props.setings);
    let defState = props.setings.value;
    if (props.options[0] && defState === undefined) {
        defState = props.options[0].value;
        props.setSettings({
            label: props.options[0].label,
            value: props.options[0].value,
            existing: true
        });
    }
    const [state, setState] = useState(defState);
    const handleChangeState = useCallback(
        (value) => {
            setState(value);
            const option = (props.options || []).find(
                option => option.value === value);
            if (option) {
                props.setSettings({
                    label: option.label,
                    value: option.value,
                    existing: true
                });
            }
        }, [props]);
    return (
        <Select
            options={props.options}
            onChange={handleChangeState}
            value={state}
        ></Select>
    )
}