import React, {useCallback, useState} from "react";
import {Banner, Button, Caption, Card, Layout, Link, Modal, TextContainer} from "@shopify/polaris";
import * as Redirect from "@shopify/app-bridge/actions/Navigation/Redirect";
import axios from 'axios';
import CampaignSettings from "./CampaignSettings";

export default function Integrtion(props) {
    const redirect = props.redirect;
    const geoOptions = [
        {
            "value": "US",
            "label": "United States"
        },
        {
            "value": "ET",
            "label": "Ethiopia"
        },
        {
            "value": "BF",
            "label": "Burkina Faso"
        },
        {
            "value": "DJ",
            "label": "Djibouti"
        },
        {
            "value": "BI",
            "label": "Burundi"
        },
        {
            "value": "BJ",
            "label": "Benin"
        },
        {
            "value": "ZA",
            "label": "South Africa"
        },
        {
            "value": "BW",
            "label": "Botswana"
        },
        {
            "value": "DZ",
            "label": "Algeria"
        },
        {
            "value": "YT",
            "label": "Mayotte"
        },
        {
            "value": "RW",
            "label": "Rwanda"
        },
        {
            "value": "TZ",
            "label": "Tanzania"
        },
        {
            "value": "CM",
            "label": "Cameroon"
        },
        {
            "value": "NA",
            "label": "Namibia"
        },
        {
            "value": "NE",
            "label": "Niger"
        },
        {
            "value": "NG",
            "label": "Nigeria"
        },
        {
            "value": "TN",
            "label": "Tunisia"
        },
        {
            "value": "RE",
            "label": "Réunion"
        },
        {
            "value": "LR",
            "label": "Liberia"
        },
        {
            "value": "LS",
            "label": "Lesotho"
        },
        {
            "value": "TG",
            "label": "Togo"
        },
        {
            "value": "TD",
            "label": "Chad"
        },
        {
            "value": "ER",
            "label": "Eritrea"
        },
        {
            "value": "LY",
            "label": "Libya"
        },
        {
            "value": "GW",
            "label": "Guinea-Bissau"
        },
        {
            "value": "ZM",
            "label": "Zambia"
        },
        {
            "value": "CI",
            "label": "Ivory Coast"
        },
        {
            "value": "EH",
            "label": "Western Sahara"
        },
        {
            "value": "GQ",
            "label": "Equatorial Guinea"
        },
        {
            "value": "EG",
            "label": "Egypt"
        },
        {
            "value": "SL",
            "label": "Sierra Leone"
        },
        {
            "value": "CG",
            "label": "Congo Republic"
        },
        {
            "value": "CF",
            "label": "Central African Republic"
        },
        {
            "value": "AO",
            "label": "Angola"
        },
        {
            "value": "CD",
            "label": "DR Congo"
        },
        {
            "value": "GA",
            "label": "Gabon"
        },
        {
            "value": "GN",
            "label": "Guinea"
        },
        {
            "value": "GM",
            "label": "Gambia"
        },
        {
            "value": "ZW",
            "label": "Zimbabwe"
        },
        {
            "value": "CV",
            "label": "Cabo Verde"
        },
        {
            "value": "GH",
            "label": "Ghana"
        },
        {
            "value": "SZ",
            "label": "Eswatini"
        },
        {
            "value": "MG",
            "label": "Madagascar"
        },
        {
            "value": "MA",
            "label": "Morocco"
        },
        {
            "value": "KE",
            "label": "Kenya"
        },
        {
            "value": "SS",
            "label": "South Sudan"
        },
        {
            "value": "ML",
            "label": "Mali"
        },
        {
            "value": "KM",
            "label": "Comoros"
        },
        {
            "value": "ST",
            "label": "São Tomé and Príncipe"
        },
        {
            "value": "MU",
            "label": "Mauritius"
        },
        {
            "value": "MW",
            "label": "Malawi"
        },
        {
            "value": "SH",
            "label": "Saint Helena"
        },
        {
            "value": "SO",
            "label": "Somalia"
        },
        {
            "value": "SN",
            "label": "Senegal"
        },
        {
            "value": "MR",
            "label": "Mauritania"
        },
        {
            "value": "SC",
            "label": "Seychelles"
        },
        {
            "value": "UG",
            "label": "Uganda"
        },
        {
            "value": "SD",
            "label": "Sudan"
        },
        {
            "value": "MZ",
            "label": "Mozambique"
        },
        {
            "value": "DO",
            "label": "Dominican Republic"
        },
        {
            "value": "DM",
            "label": "Dominica"
        },
        {
            "value": "BB",
            "label": "Barbados"
        },
        {
            "value": "BL",
            "label": "Saint Barthélemy"
        },
        {
            "value": "BM",
            "label": "Bermuda"
        },
        {
            "value": "HT",
            "label": "Haiti"
        },
        {
            "value": "SV",
            "label": "El Salvador"
        },
        {
            "value": "JM",
            "label": "Jamaica"
        },
        {
            "value": "VC",
            "label": "Saint Vincent and the Grenadines"
        },
        {
            "value": "HN",
            "label": "Honduras"
        },
        {
            "value": "BQ",
            "label": "Bonaire, Sint Eustatius, and Saba"
        },
        {
            "value": "BS",
            "label": "Bahamas"
        },
        {
            "value": "BZ",
            "label": "Belize"
        },
        {
            "value": "PR",
            "label": "Puerto Rico"
        },
        {
            "value": "NI",
            "label": "Nicaragua"
        },
        {
            "value": "LC",
            "label": "Saint Lucia"
        },
        {
            "value": "TT",
            "label": "Trinidad and Tobago"
        },
        {
            "value": "SX",
            "label": "Sint Maarten"
        },
        {
            "value": "VG",
            "label": "British Virgin Islands"
        },
        {
            "value": "PA",
            "label": "Panama"
        },
        {
            "value": "TC",
            "label": "Turks and Caicos Islands"
        },
        {
            "value": "PM",
            "label": "Saint Pierre and Miquelon"
        },
        {
            "value": "GT",
            "label": "Guatemala"
        },
        {
            "value": "AG",
            "label": "Antigua and Barbuda"
        },
        {
            "value": "GP",
            "label": "Guadeloupe"
        },
        {
            "value": "AI",
            "label": "Anguilla"
        },
        {
            "value": "VI",
            "label": "U.S. Virgin Islands"
        },
        {
            "value": "CA",
            "label": "Canada"
        },
        {
            "value": "GD",
            "label": "Grenada"
        },
        {
            "value": "AW",
            "label": "Aruba"
        },
        {
            "value": "CR",
            "label": "Costa Rica"
        },
        {
            "value": "GL",
            "label": "Greenland"
        },
        {
            "value": "CW",
            "label": "Curaçao"
        },
        {
            "value": "CU",
            "label": "Cuba"
        },
        {
            "value": "MF",
            "label": "Saint Martin"
        },
        {
            "value": "KN",
            "label": "St Kitts and Nevis"
        },
        {
            "value": "MQ",
            "label": "Martinique"
        },
        {
            "value": "MS",
            "label": "Montserrat"
        },
        {
            "value": "KY",
            "label": "Cayman Islands"
        },
        {
            "value": "MX",
            "label": "Mexico"
        },
        {
            "value": "WF",
            "label": "Wallis and Futuna"
        },
        {
            "value": "WS",
            "label": "Samoa"
        },
        {
            "value": "FJ",
            "label": "Fiji"
        },
        {
            "value": "FM",
            "label": "Federated States of Micronesia"
        },
        {
            "value": "PW",
            "label": "Palau"
        },
        {
            "value": "TV",
            "label": "Tuvalu"
        },
        {
            "value": "NC",
            "label": "New Caledonia"
        },
        {
            "value": "TL",
            "label": "East Timor"
        },
        {
            "value": "TO",
            "label": "Tonga"
        },
        {
            "value": "NF",
            "label": "Norfolk Island"
        },
        {
            "value": "NZ",
            "label": "New Zealand"
        },
        {
            "value": "PF",
            "label": "French Polynesia"
        },
        {
            "value": "TK",
            "label": "Tokelau"
        },
        {
            "value": "NR",
            "label": "Nauru"
        },
        {
            "value": "PN",
            "label": "Pitcairn Islands"
        },
        {
            "value": "NU",
            "label": "Niue"
        },
        {
            "value": "PG",
            "label": "Papua New Guinea"
        },
        {
            "value": "CK",
            "label": "Cook Islands"
        },
        {
            "value": "GU",
            "label": "Guam"
        },
        {
            "value": "AS",
            "label": "American Samoa"
        },
        {
            "value": "CX",
            "label": "Christmas Island"
        },
        {
            "value": "AU",
            "label": "Australia"
        },
        {
            "value": "VU",
            "label": "Vanuatu"
        },
        {
            "value": "KI",
            "label": "Kiribati"
        },
        {
            "value": "MH",
            "label": "Marshall Islands"
        },
        {
            "value": "UM",
            "label": "U.S. Minor Outlying Islands"
        },
        {
            "value": "MP",
            "label": "Northern Mariana Islands"
        },
        {
            "value": "SB",
            "label": "Solomon Islands"
        },
        {
            "value": "AQ",
            "label": "Antarctica"
        },
        {
            "value": "TF",
            "label": "French Southern Territories"
        },
        {
            "value": "BV",
            "label": "Bouvet Island"
        },
        {
            "value": "GS",
            "label": "South Georgia and the South Sandwich Islands"
        },
        {
            "value": "HM",
            "label": "Heard Island and McDonald Islands"
        },
        {
            "value": "BD",
            "label": "Bangladesh"
        },
        {
            "value": "MN",
            "label": "Mongolia"
        },
        {
            "value": "BN",
            "label": "Brunei"
        },
        {
            "value": "BH",
            "label": "Bahrain"
        },
        {
            "value": "BT",
            "label": "Bhutan"
        },
        {
            "value": "HK",
            "label": "Hong Kong"
        },
        {
            "value": "JO",
            "label": "Hashemite Kingdom of Jordan"
        },
        {
            "value": "PS",
            "label": "Palestine"
        },
        {
            "value": "LB",
            "label": "Lebanon"
        },
        {
            "value": "LA",
            "label": "Laos"
        },
        {
            "value": "TW",
            "label": "Taiwan"
        },
        {
            "value": "TR",
            "label": "Turkey"
        },
        {
            "value": "LK",
            "label": "Sri Lanka"
        },
        {
            "value": "IQ",
            "label": "Iraq"
        },
        {
            "value": "MV",
            "label": "Maldives"
        },
        {
            "value": "TJ",
            "label": "Tajikistan"
        },
        {
            "value": "TH",
            "label": "Thailand"
        },
        {
            "value": "NP",
            "label": "Nepal"
        },
        {
            "value": "PK",
            "label": "Pakistan"
        },
        {
            "value": "PH",
            "label": "Philippines"
        },
        {
            "value": "TM",
            "label": "Turkmenistan"
        },
        {
            "value": "AE",
            "label": "United Arab Emirates"
        },
        {
            "value": "CN",
            "label": "China"
        },
        {
            "value": "AF",
            "label": "Afghanistan"
        },
        {
            "value": "CC",
            "label": "Cocos [Keeling] Islands"
        },
        {
            "value": "JP",
            "label": "Japan"
        },
        {
            "value": "IR",
            "label": "Iran"
        },
        {
            "value": "AM",
            "label": "Armenia"
        },
        {
            "value": "SY",
            "label": "Syria"
        },
        {
            "value": "VN",
            "label": "Vietnam"
        },
        {
            "value": "GE",
            "label": "Georgia"
        },
        {
            "value": "IL",
            "label": "Israel"
        },
        {
            "value": "IO",
            "label": "British Indian Ocean Territory"
        },
        {
            "value": "IN",
            "label": "India"
        },
        {
            "value": "AZ",
            "label": "Azerbaijan"
        },
        {
            "value": "ID",
            "label": "Indonesia"
        },
        {
            "value": "OM",
            "label": "Oman"
        },
        {
            "value": "KG",
            "label": "Kyrgyzstan"
        },
        {
            "value": "UZ",
            "label": "Uzbekistan"
        },
        {
            "value": "MM",
            "label": "Myanmar"
        },
        {
            "value": "SG",
            "label": "Singapore"
        },
        {
            "value": "MO",
            "label": "Macao"
        },
        {
            "value": "KH",
            "label": "Cambodia"
        },
        {
            "value": "QA",
            "label": "Qatar"
        },
        {
            "value": "KR",
            "label": "South Korea"
        },
        {
            "value": "KP",
            "label": "North Korea"
        },
        {
            "value": "KW",
            "label": "Kuwait"
        },
        {
            "value": "KZ",
            "label": "Kazakhstan"
        },
        {
            "value": "SA",
            "label": "Saudi Arabia"
        },
        {
            "value": "MY",
            "label": "Malaysia"
        },
        {
            "value": "YE",
            "label": "Yemen"
        },
        {
            "value": "BE",
            "label": "Belgium"
        },
        {
            "value": "FR",
            "label": "France"
        },
        {
            "value": "BG",
            "label": "Bulgaria"
        },
        {
            "value": "BA",
            "label": "Bosnia and Herzegovina"
        },
        {
            "value": "XK",
            "label": "Kosovo"
        },
        {
            "value": "HR",
            "label": "Croatia"
        },
        {
            "value": "DE",
            "label": "Germany"
        },
        {
            "value": "HU",
            "label": "Hungary"
        },
        {
            "value": "JE",
            "label": "Jersey"
        },
        {
            "value": "SJ",
            "label": "Svalbard and Jan Mayen"
        },
        {
            "value": "FI",
            "label": "Finland"
        },
        {
            "value": "BY",
            "label": "Belarus"
        },
        {
            "value": "DK",
            "label": "Denmark"
        },
        {
            "value": "RU",
            "label": "Russia"
        },
        {
            "value": "NL",
            "label": "Netherlands"
        },
        {
            "value": "PT",
            "label": "Portugal"
        },
        {
            "value": "NO",
            "label": "Norway"
        },
        {
            "value": "LI",
            "label": "Liechtenstein"
        },
        {
            "value": "LV",
            "label": "Latvia"
        },
        {
            "value": "LT",
            "label": "Republic of Lithuania"
        },
        {
            "value": "LU",
            "label": "Luxembourg"
        },
        {
            "value": "ES",
            "label": "Spain"
        },
        {
            "value": "FO",
            "label": "Faroe Islands"
        },
        {
            "value": "PL",
            "label": "Poland"
        },
        {
            "value": "VA",
            "label": "Vatican City"
        },
        {
            "value": "CH",
            "label": "Switzerland"
        },
        {
            "value": "GR",
            "label": "Greece"
        },
        {
            "value": "EE",
            "label": "Estonia"
        },
        {
            "value": "IS",
            "label": "Iceland"
        },
        {
            "value": "AL",
            "label": "Albania"
        },
        {
            "value": "IT",
            "label": "Italy"
        },
        {
            "value": "GG",
            "label": "Guernsey"
        },
        {
            "value": "CZ",
            "label": "Czechia"
        },
        {
            "value": "CY",
            "label": "Cyprus"
        },
        {
            "value": "IM",
            "label": "Isle of Man"
        },
        {
            "value": "GB",
            "label": "United Kingdom"
        },
        {
            "value": "AX",
            "label": "Åland"
        },
        {
            "value": "AD",
            "label": "Andorra"
        },
        {
            "value": "IE",
            "label": "Ireland"
        },
        {
            "value": "GI",
            "label": "Gibraltar"
        },
        {
            "value": "ME",
            "label": "Montenegro"
        },
        {
            "value": "MD",
            "label": "Republic of Moldova"
        },
        {
            "value": "RO",
            "label": "Romania"
        },
        {
            "value": "MC",
            "label": "Monaco"
        },
        {
            "value": "RS",
            "label": "Serbia"
        },
        {
            "value": "MK",
            "label": "North Macedonia"
        },
        {
            "value": "SK",
            "label": "Slovakia"
        },
        {
            "value": "MT",
            "label": "Malta"
        },
        {
            "value": "SI",
            "label": "Slovenia"
        },
        {
            "value": "SM",
            "label": "San Marino"
        },
        {
            "value": "UA",
            "label": "Ukraine"
        },
        {
            "value": "SE",
            "label": "Sweden"
        },
        {
            "value": "AT",
            "label": "Austria"
        },
        {
            "value": "PY",
            "label": "Paraguay"
        },
        {
            "value": "CO",
            "label": "Colombia"
        },
        {
            "value": "VE",
            "label": "Venezuela"
        },
        {
            "value": "CL",
            "label": "Chile"
        },
        {
            "value": "SR",
            "label": "Suriname"
        },
        {
            "value": "BO",
            "label": "Bolivia"
        },
        {
            "value": "EC",
            "label": "Ecuador"
        },
        {
            "value": "GF",
            "label": "French Guiana"
        },
        {
            "value": "AR",
            "label": "Argentina"
        },
        {
            "value": "GY",
            "label": "Guyana"
        },
        {
            "value": "BR",
            "label": "Brazil"
        },
        {
            "value": "PE",
            "label": "Peru"
        },
        {
            "value": "UY",
            "label": "Uruguay"
        },
        {
            "value": "FK",
            "label": "Falkland Islands"
        }
    ];
    const relevant_geoOptions = geoOptions.slice();
    const retargeting_geoOptions = geoOptions.slice();

    const [budgetValue, setBudget] = useState(props.current_shop.feed.integration.data.new_auditory.budget + '');
    const [relevant_budgetValue, relevant_setBudget] = useState(props.current_shop.feed.integration.data.relevant.budget + '');
    const [retargeting_budgetValue, retargeting_setBudget] = useState(props.current_shop.feed.integration.data.retargeting.budget + '');

    const [campaignRun, setCampaignRun] = useState(props.current_shop.feed.integration.data.new_auditory.status);
    const [retargeting_campaignRun, retargeting_setCampaignRun] = useState(props.current_shop.feed.integration.data.retargeting.status);
    const [relevant_campaignRun, relevant_setCampaignRun] = useState(props.current_shop.feed.integration.data.relevant.status);

    const [selectedOptionsGeo, setSelectedOptionsGeo] = useState(props.current_shop.feed.integration.data.new_auditory.geo);
    const [selectedOptionsGeoRel, setSelectedOptionsGeoRel] = useState(props.current_shop.feed.integration.data.relevant.geo);
    const [selectedOptionsGeoRet, setSelectedOptionsGeoRet] = useState(props.current_shop.feed.integration.data.retargeting.geo);

    const premium = props.current_shop.premium;
    const liStyle = {
        fontSize: '30px',
        marginBottom: '10px'
    };
    const divStyle = {
        position: 'relative',
        top: '-5px'
    };

    const [sheetActive, setSheetActive] = useState(false);
    const toggleSheetOpen = useCallback(
        () => {
            if (premium) {
                window.ga('send', 'event', 'Click', 'Open', 'NewAuditory');
                if (window.fbq) {
                    fbq('trackCustom', 'Open_NewAuditory');
                }
                setSheetActive((sheetActive) => !sheetActive);
            } else {
                handleChange();
            }
        },
        []
    );

    function toggleSheetClose() {
        toggleSheetOpen();
    }

    function toggleSheetSave() {
        if (premium) {
            toggleSheetOpen();
            axios.defaults.xsrfCookieName = 'csrftoken';
            axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
            axios.post('/shopify/fb_integration/campaign?type=new', {
                data: {
                    geo: selectedOptionsGeo,
                    budget: budgetValue,
                    status: campaignRun
                },
                shop: props.current_shop.domain
            }).then(function (response) {
                let url = (response.data || {}).url;
                if (url) {
                    redirect.dispatch(Redirect.Action.APP, url);
                }
            });
        }
        else {
            toggleSheetClose();
            handleChange();
        }
    }


    const [relevant_sheetActive, relevant_setSheetActive] = useState(false);
    const relevant_toggleSheetOpen = useCallback(
        () => {
            if (premium) {
                window.ga('send', 'event', 'Click', 'Open', 'Relevant');
                if (window.fbq) {
                    fbq('trackCustom', 'Open_Relevant');
                }
                relevant_setSheetActive((relevant_sheetActive) => !relevant_sheetActive);
            } else {
                handleChange();
            }
        },
        []
    );

    function relevant_toggleSheetClose() {
        relevant_toggleSheetOpen();
    }

    function relevant_toggleSheetSave() {
        if (premium) {
            relevant_toggleSheetOpen();
            axios.defaults.xsrfCookieName = 'csrftoken';
            axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
            axios.post('/shopify/fb_integration/campaign?type=rel', {
                data: {
                    geo: selectedOptionsGeoRel,
                    budget: relevant_budgetValue,
                    status: relevant_campaignRun
                },
                shop: props.current_shop.domain
            }).then(function (response) {
                let url = (response.data || {}).url;
                if (url) {
                    redirect.dispatch(Redirect.Action.APP, url);
                }
            });
        }
        else {
            relevant_toggleSheetClose();
            handleChange();
        }
    }

    const [retargeting_sheetActive, retargeting_setSheetActive] = useState(false);
    const retargeting_toggleSheetOpen = useCallback(
        () => {
            if (premium) {
                window.ga('send', 'event', 'Click', 'Open', 'Relevant');
                if (window.fbq) {
                    fbq('trackCustom', 'Open_Relevant');
                }
                retargeting_setSheetActive((relevant_sheetActive) => !relevant_sheetActive);
            } else {
                handleChange();
            }
        },
        []
    );

    function retargeting_toggleSheetClose() {
        retargeting_toggleSheetOpen();
    }

    function retargeting_toggleSheetSave() {
        if (premium) {
            retargeting_toggleSheetOpen();
            axios.defaults.xsrfCookieName = 'csrftoken';
            axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
            axios.post('/shopify/fb_integration/campaign?type=ret', {
                data: {
                    geo: selectedOptionsGeoRet,
                    budget: retargeting_budgetValue,
                    status: retargeting_campaignRun
                },
                shop: props.current_shop.domain
            }).then(function (response) {
                let url = (response.data || {}).url;
                if (url) {
                    redirect.dispatch(Redirect.Action.APP, url);
                }
            });
        }
        else {
            retargeting_toggleSheetClose();
            handleChange();
        }
    }


    const [active, setActive] = useState(false);
    const handleChange = useCallback(() => setActive(!active), [active]);

    function upgrade() {
        window.ga('send', 'event', 'Order', 'Upgrade', 'Collections');
        window.ga('ec:addProduct', {
            'id': '1',
            'name': 'Premium',
            'price': '29.00',
            'variant': 'Collections',
            'quantity': 1
        });
        window.ga('ec:setAction', 'checkout', {
            'step': 1,
            'id': window.t
        });
        if (window.fbq) {
            fbq('track', 'InitiateCheckout', {
                content_ids: [1],
                content_name: 'Premium',
                content_type: 'product',
                content_category: 'Collections',
                contents: [
                    {
                        'id': '1',
                        'quantity': 1
                    }
                ],
                currency: "USD",
                value: 29.00
            });
        }
        redirect.dispatch(Redirect.Action.APP, props.current_shop.billing);
    }

    function statusChangeCallback(
        response,
        recall
    ) {
        if (response.status === 'connected') {
            redirect.dispatch(Redirect.Action.APP, props.current_shop.fb_integration);
        }
        else if ((response.status === 'unknown' || response.status === 'not_authorized') && recall !== true) {
            FB.login(
                function (response) {
                    statusChangeCallback(response, true);
                }, {
                    scope: 'email,ads_management,business_management,manage_pages',
                    auth_type: 'rerequest',
                    return_scopes: true
                }
            );
        }
    }

    function connectFb() {
        FB.getLoginStatus(function (response) {
            statusChangeCallback(response);
        });
    }

    function disonnectFb() {
        redirect.dispatch(Redirect.Action.APP, props.current_shop.fb_disconect);
    }

    function fb_pixel() {
        if (props.current_shop.feed.integration.pixel) {
            const src = "https://www.facebook.com/tr?id=" + props.current_shop.feed.integration.pixel + "&ev=PageView";
            return (<li style={liStyle}>
                <div style={divStyle}>
                    <Banner title="Check Facebook Pixel ID" status="info">
                        <p style={{
                            fontSize: '16px'
                        }}>Check the Pixel ID setting in your store. &nbsp;
                        </p>
                        <p style={{
                            fontSize: '16px',
                            marginTop: '5px'
                        }}>Your Pixel ID <b>{props.current_shop.feed.integration.pixel}</b></p>
                        <p style={{
                            fontSize: '16px',
                            marginTop: '5px'
                        }}>
                            <Link
                                url="https://help.shopify.com/en/manual/promoting-marketing/analyze-marketing/facebook-pixel#add-a-facebook-pixel-id-to-your-online-store-preferences"
                                external>
                                Learn how to add your Pixel ID.
                            </Link>
                        </p>
                    </Banner>
                    <img src={src} height="1" width="1" style={{
                        display: 'none'
                    }}/>
                </div>
            </li>);
        }
        else {
            return (null);
        }
    }

    if (props.current_shop.feed.integration) {
        if (props.current_shop.feed.integration.complite) {
            return (
                <Layout.AnnotatedSection
                    title={props.current_shop.feed.integration.text.title}
                    description={props.current_shop.feed.integration.text.description}>
                    <Card sectioned title={props.current_shop.feed.integration.text.sectioned_title}>
                        <ol>
                            {fb_pixel()}
                            <li style={liStyle}>
                                <div style={divStyle}>
                                    <Button external={true} fullWidth={true} primary={true}
                                            onClick={toggleSheetOpen}>
                                        {props.current_shop.feed.integration.text.buttons.new_auditory}
                                    </Button>
                                </div>
                            </li>
                            <li style={liStyle}>
                                <div style={divStyle}>
                                    <Button external={true} fullWidth={true} primary={true}
                                            onClick={retargeting_toggleSheetOpen}>
                                        {props.current_shop.feed.integration.text.buttons.retargeting}
                                    </Button>
                                </div>
                            </li>
                            <li style={liStyle}>
                                <div style={divStyle}>
                                    <Button external={true} fullWidth={true} primary={true}
                                            onClick={relevant_toggleSheetOpen}>
                                        {props.current_shop.feed.integration.text.buttons.relevant}
                                    </Button>
                                </div>
                            </li>
                        </ol>
                        <Caption>To disconnect facebook click on the <Link onClick={disonnectFb}>link </Link></Caption>
                    </Card>

                    <CampaignSettings
                        sheetActive={sheetActive}
                        toggleSheetClose={toggleSheetClose}
                        toggleSheetSave={toggleSheetSave}
                        geoOptions={geoOptions}
                        selectedOptionsGeo={selectedOptionsGeo}
                        setSelectedOptionsGeo={setSelectedOptionsGeo}
                        current_shop={props.current_shop}
                        budgetValue={budgetValue}
                        setBudget={setBudget}
                        campaignRun={campaignRun}
                        setCampaignRun={setCampaignRun}
                        sheet={props.current_shop.feed.integration.new_auditory}
                    />
                    <CampaignSettings
                        sheetActive={retargeting_sheetActive}
                        toggleSheetClose={retargeting_toggleSheetClose}
                        toggleSheetSave={retargeting_toggleSheetSave}
                        geoOptions={retargeting_geoOptions}
                        selectedOptionsGeo={selectedOptionsGeoRet}
                        setSelectedOptionsGeo={setSelectedOptionsGeoRet}
                        current_shop={props.current_shop}
                        budgetValue={retargeting_budgetValue}
                        setBudget={retargeting_setBudget}
                        campaignRun={retargeting_campaignRun}
                        setCampaignRun={retargeting_setCampaignRun}
                        sheet={props.current_shop.feed.integration.retargeting}
                    />
                    <CampaignSettings
                        sheetActive={relevant_sheetActive}
                        toggleSheetClose={relevant_toggleSheetClose}
                        toggleSheetSave={relevant_toggleSheetSave}
                        geoOptions={relevant_geoOptions}
                        selectedOptionsGeo={selectedOptionsGeoRel}
                        setSelectedOptionsGeo={setSelectedOptionsGeoRel}
                        current_shop={props.current_shop}
                        budgetValue={relevant_budgetValue}
                        setBudget={relevant_setBudget}
                        campaignRun={relevant_campaignRun}
                        setCampaignRun={relevant_setCampaignRun}
                        sheet={props.current_shop.feed.integration.relevant}
                    />
                    <Modal
                        open={active}
                        onClose={handleChange}
                        title="Upgrade to Premium Membershi"
                        primaryAction={{
                            content: 'Upgrade to Premium Membership',
                            onAction: upgrade
                        }}
                        secondaryActions={[
                            {
                                content: 'Close',
                                onAction: handleChange
                            }
                        ]}
                    >
                        <Modal.Section>
                            <TextContainer>
                                <p>
                                    This option is available only in premium.
                                </p>
                            </TextContainer>
                        </Modal.Section>
                    </Modal>
                </Layout.AnnotatedSection>
            )
        }
        else {
            return (
                <Layout.AnnotatedSection
                    title={props.current_shop.feed.integration.text.title}
                    description={props.current_shop.feed.integration.text.description}>
                    <Card sectioned title={props.current_shop.feed.integration.text.sectioned_title}>
                        <Button external={true} fullWidth={true} primary={true} onClick={connectFb}>
                            {props.current_shop.feed.integration.text.buttons.activate}
                        </Button>
                    </Card>
                </Layout.AnnotatedSection>
            )
        }
    }
    return (null);
}
