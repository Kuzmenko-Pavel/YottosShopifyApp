import React, {useCallback, useState} from 'react';
import {ChoiceList} from "@shopify/polaris";
import SelectExists from './SelectExists';
import Create from './Create';

export default function Choicer(props) {
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
                                      checkSettings={props.checkSettings} type={props.type} error={""}/>
                    ),
                    [props]
                );
            }
            else {
                choice.renderChildren = useCallback(
                    isSelected => isSelected && (
                        <Create setSettings={props.setSettings} setings={props.setings} createData={props.createData}
                                checkSettings={props.checkSettings} type={props.type} error={""}
                        />
                    ),
                    [props]
                );
            }
            return choice;
        }
    );
    let Choice_List = <ChoiceList choices={choices}
                                  selected={state}
                                  onChange={handleChangeState}
    />;
    if (choices.length === 1) {
        Choice_List = <SelectExists options={props.options} setSettings={props.setSettings} setings={props.setings}
                                    checkSettings={props.checkSettings} type={props.type} error={props.error}/>;
    }
    return Choice_List;
}
