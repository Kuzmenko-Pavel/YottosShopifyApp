import React, {useCallback, useState} from 'react';
import {ChoiceList} from "@shopify/polaris";
import SelectExists from './SelectExists';
import CreateFunding from './CreateFunding';

export default function ChoicerFunding(props) {
    let defState = 'create';
    if (props.options[0]) {
        defState = 'existing';
    }
    const [state, setState] = useState([defState]);
    const handleChangeState = useCallback(
        (value) => {
            setState(value);
        }, []);
    const choices = props.choices.map(
        choice => {
            if (choice.value === 'existing') {
                choice.renderChildren = useCallback(
                    isSelected => isSelected && (
                        <SelectExists options={props.options} setSettings={props.setSettings} setings={props.setings}
                                      checkSettings={props.checkSettings} type={props.type}/>
                    ),
                    [props]
                );
            }
            else {
                choice.renderChildren = useCallback(
                    isSelected => isSelected && (
                        <CreateFunding setSettings={props.setSettings} setings={props.setings}
                                       createData={props.createData}
                                       checkSettings={props.checkSettings} type={props.type}
                        />
                    ),
                    [props]
                );
            }
            return choice;
        }
    );
    return <ChoiceList choices={choices}
                       selected={state}
                       onChange={handleChangeState}
    />;
}
