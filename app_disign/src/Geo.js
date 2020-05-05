import React, {useCallback, useState} from 'react';
import {Autocomplete, Heading, SettingToggle, Stack, Tag} from '@shopify/polaris';

export default function Geo(props) {
    const paginationInterval = 25;
    const [inputValue, setInputValue] = useState('');
    const [options, setOptions] = useState(props.geo);
    const [visibleOptionIndex, setVisibleOptionIndex] = useState(
        paginationInterval
    );

    const handleLoadMoreResults = useCallback(() => {
        const nextVisibleOptionIndex = visibleOptionIndex + paginationInterval;
        if (nextVisibleOptionIndex <= options.length - 1) {
            setVisibleOptionIndex(nextVisibleOptionIndex);
        }
    }, [visibleOptionIndex]);

    const removeTag = useCallback(
        (tag) => () => {
            const options = [...props.selectedOptions];
            options.splice(options.indexOf(tag), 1);
            props.setSelectedOptions(options);
        },
        [props.selectedOptions]
    );

    const updateText = useCallback(
        (value) => {
            setInputValue(value);

            if (value === '') {
                setOptions(props.geo);
                return;
            }

            const filterRegex = new RegExp(value, 'i');
            const resultOptions = options.filter((option) =>
                option.label.match(filterRegex)
            );

            let endIndex = resultOptions.length - 1;
            if (resultOptions.length === 0) {
                endIndex = 0;
            }
            setOptions(resultOptions);
        },
        [props.geo]
    );

    const textField = (
        <Autocomplete.TextField
            onChange={updateText}
            value={inputValue}
            placeholder="Country Geo Targeting"
        />
    );

    const hasSelectedOptions = props.selectedOptions.length > 0;

    const tagsMarkup = hasSelectedOptions
        ? props.selectedOptions.map((option) => {
            let tagLabel = props.geo.filter((opt) =>
                opt.value === option
            )[0] || {
                value: "",
                label: ""
            };
            return (
                <Tag key={`option${option}`} onRemove={removeTag(option)}>
                    {tagLabel.label}
                </Tag>
            );
        })
        : null;
    const optionList = options.slice(0, visibleOptionIndex);
    const selectedTagMarkup = hasSelectedOptions ? (
        <Stack spacing="extraTight">{tagsMarkup}</Stack>
    ) : null;

    return (
        <SettingToggle>
            <Stack vertical>
                <Heading>Geo Targeting</Heading>
                {selectedTagMarkup}
                <Autocomplete
                    allowMultiple
                    options={optionList}
                    selected={props.selectedOptions}
                    textField={textField}
                    onSelect={props.setSelectedOptions}
                    listTitle="Geo Tags"
                    onLoadMoreResults={handleLoadMoreResults}
                />
            </Stack>
        </SettingToggle>
    );
}
