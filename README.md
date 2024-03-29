# HomeAssistant-DMIPollen

### The unofficial DMI API does not seem to be updated anymore (Last sample 2023.11.19). So this custom component is not getting any data right now. 
Looking at pulling data from https://www.astma-allergi.dk/umbraco/Api/PollenApi/GetPollenFeed instead, but my time is limited, so if anyone have some spare time, feel free to give it a shot. 

-------------------------------------------------
Home Assistant Custom Component showing pollen data from dmi.dk (Danmarks Meteorologiske Institut) by use of the REST response from: [https://www.dmi.dk/dmidk_byvejrWS/rest/texts/forecast/pollen/Danmark/](https://www.dmi.dk/dmidk_byvejrWS/rest/texts/forecast/pollen/Danmark/)

<img src="images/hapollenview.png">
See more screenshots in the image folder

## Installation

### Manual Installation
  1. Copy `dmipollen` folder into the custom_components folder of your home assistant configuration directory.
  2. Restart Home Assistant.
  3. Configure the `dmipollen` sensor in configuration.yaml as explained futher down.
  4. Restart Home Assistant.

### Installation via HACS (Home Assistant Community Store) [![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg?style=for-the-badge)](https://github.com/custom-components/hacs)
  1. Ensure that [HACS](https://hacs.xyz/) is installed.
  2. Open HACS and add `https://github.com/ChristofferG/homeassistant-dmipollen` as a Custom repository, and choose Integration.
  3. Click DMI Pollen and click "Install this repository in HACS".
  4. Restart Home Assistant.
  5. Configure the `dmipollen` sensor in configuration.yaml as explained futher down.
  6. Restart Home Assistant.

## Configuration

`dmipollen` can for now only be configured via configuration.yaml. Working on a Config flow.

```yaml
# Example configuration.yaml entry

sensor:
  - platform: dmipollen
    region: viborg 
    scan_interval: 3600
    resources:
      - birk
      - bynke
      - el
      - elm
      - græs
      - hassel
      - alternaria
      - cladosporium
      - forecast
      - polleninfo
      - lastupdate
```

### CONFIGURATION PARAMETERS

|Parameter |Optional|Description
|:----------|----------|------------
| `region` | No | Measurement spot. `københavn`, `viborg` or `all` is available. `all` will include both København and Viborg.
|`scan_interval` | Yes | How offent the component will poll dmi.dk. The data on dmi.dk is only updated once a day, typical in the afternoon. The default value of the scan_interval is 3600sec (1hour)

### CONFIGURATION RESOURCES

|Resources |Optional|Description
|:----------|----------|------------
| `birk` | Yes | Return state of `birk`
|`bynke` | Yes | Return state of `bynke`
|`el` | Yes | Return state of `el`
|`elm` | Yes | Return state of `elm`
|`græs` | Yes | Return state of `græs`
|`hassel` | Yes | Return state of `hassel`
|`alternaria` | Yes | Return state of `alternaria` (Measurement only available from København)
|`cladosporium` | Yes | Return state of `cladosporium` (Measurement only available from København)
|`forecast` | Yes | Return tomorrows pollen forecast as a danish text string. E.g 'For i morgen, onsdag d. 1. juli 2020, ventes et moderat antal græspollen (mellem 10-50)'
|`polleninfo` | Yes | Return information string about how the pollen is measured.
|`lastupdate` | Yes | Return the last update timestamp as a string in the format: 'tirsdag den 30. juni 2020'

## States and attributes

Each selected recource will create a sensor the naming syntax:
* E.g. `sensor.pollen_viborg_birk` and a coreponding friendly name `Pollen Viborg Birk`

The unit of the pollen data is `ppcm` - Part Per Cubic Meter

Each sensor will have the attributes `last_update` timestamp and `attribution` with information about where the data comes from.

## Future
* As dmi.dk is working on providing free data, the source of the pollen data will properly change during the next years. See [https://confluence.govcloud.dk/display/FDAPI](https://confluence.govcloud.dk/display/FDAPI)
* Add config flow
* Add as HACS original
