import React, {useCallback, useState} from 'react';
import {Select} from "@shopify/polaris";

export default function SelectExists(props) {
    let defState = props.setings.value;
    if (props.options[0] && defState === undefined) {
        defState = props.options[0].value;
        props.setSettings(props.type, {
            label: props.options[0].label,
            value: props.options[0].value,
            existing: true
        });
    }
    else {
        props.checkSettings(props.type);
    }
    const [state, setState] = useState(defState);
    const handleChangeState = useCallback(
        (value) => {
            setState(value);
            const option = (props.options || []).find(
                option => option.value === value);
            if (option) {
                props.setSettings(props.type, {
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