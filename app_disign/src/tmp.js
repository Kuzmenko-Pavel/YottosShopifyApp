import React, {useCallback, useState} from "react";
import {Select} from "@shopify/polaris";

const [AccountSelected, setAccountSelected] = useState([]);
const handleAccountChange = useCallback((value) => setAccountSelected(value), []);

const [PixelSelected, setPixelSelected] = useState([]);
const handlePixelChange = useCallback((value) => setPixelSelected(value), []);

const [BusinessManagerSelected, setBusinessManagerSelected] = useState([default_BusinessManagerSelected]);
const handleBusinessManagerChange = useCallback(
    (value) => {
        setBusinessManagerSelected(value);
        if (value[0] === 'existing_business_manager') {
            setAccountSelected(['existing_account'])
        }
        else {
            setAccountSelected(['create_account'])
        }
    }, []);

const renderExistingAccounts = useCallback(
    isSelected => {
        if (isSelected) {
            let existingAccounts = [];
            existingBusiness.forEach(
                businesse => {
                    if (businesse.id === selectedExistingBusiness) {
                        existingAccounts = businesse.accounts;
                    }
                }
            );
            console.log(existingAccounts);
            return (
                <Select
                    options={existingAccounts}
                    onChange={handleSelectExistingBusiness}
                    value={selectedExistingBusiness}
                />
            )
        }

    },
    [
        existingBusiness,
        handleSelectExistingBusiness,
        selectedExistingBusiness
    ]
);
const renderCreateAccounts = useCallback(
    isSelected => isSelected && (null),
    []
);
const [selectedExistingBusiness, setExistingBusiness] = useState(default_existingBusiness);
const handleSelectExistingBusiness = useCallback((value) => setExistingBusiness(value), []);

const renderExistingBusinessManager = useCallback(
    isSelected => isSelected && (
        <Select
            options={existingBusiness}
            onChange={handleSelectExistingBusiness}
            value={selectedExistingBusiness}
        />
    ),
    [
        existingBusiness,
        handleSelectExistingBusiness,
        selectedExistingBusiness
    ]
);
const renderCreateBusinessManager = useCallback(
    isSelected => isSelected && (null),
    []
);
