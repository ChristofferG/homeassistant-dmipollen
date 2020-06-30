# HomeAssistant-DMIPollen
[![hacs_badge](https://img.shields.io/badge/HACS-Default-orange.svg)](https://github.com/custom-components/hacs)

Home Assistant Custom Component showing pollen data from dmi.dk (Danmarks Meteorologiske Institut) by use of the REST response from: [https://www.dmi.dk/dmidk_byvejrWS/rest/texts/forecast/pollen/Danmark/](https://www.dmi.dk/dmidk_byvejrWS/rest/texts/forecast/pollen/Danmark/)

## Installation

### Manual Installation
  1. Copy dmipollen folder into the custom_components folder of your home assistant configuration directory.
  2. Restart Home Assistant.
  3. Configure the `dmipollen` sensor in configuration.yaml as explained futher down.
  4. Restart Home Assistant.

### Installation via HACS (Home Assistant Community Store)
  1. Ensure that [HACS](https://hacs.xyz/) is installed.
  2. Search for and install the `dmipollen` integration.
  3. Confiure the `dmipollen` sensor.
  4. Restart Home Assistant.


## Configuration

`dmipollen` can only be configured via configuration.yaml

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
|`alternaria` | Yes | Return state of `alternaria` (Meassueremnt only available from København)
|`cladosporium` | Yes | Return state of `cladosporium` (Meassuremnet only available from København)
|`forecast` | Yes | Return tomorrows pollenforecast as a danish text string
|`polleninfo` | Yes | Return information string about the pollen is meassured
|`lastupdate` | Yes | Return the last update timestamp as a string in the format: 'tirsdag den 30. juni 2020'

## States and attributes

A sensor will be created with the naming syntax:
* sensor.pollen_viborg_birk and a Friendly name: Pollen Viborg Birk

Each sensor will have the attributes `last_update` timestamp and `attribution` with information about where the data comes from.

## Future
---
As dmi.dk is working on providing free data the source of the pollen data will properly change during the next years. See [https://confluence.govcloud.dk/display/FDAPI](https://confluence.govcloud.dk/display/FDAPI)