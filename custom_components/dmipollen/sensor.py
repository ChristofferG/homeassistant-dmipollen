"""
Reading pollen data and forecast from DMI.dk

configuration.yaml

sensor:
  - platform: dmipollen
    region: all //all, viborg or københavn 
    scan_interval: 30
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
"""

import logging
from datetime import datetime, timedelta
import voluptuous as vol
import hashlib

from homeassistant.components.sensor import PLATFORM_SCHEMA, ENTITY_ID_FORMAT
import homeassistant.helpers.config_validation as cv
from homeassistant.const import (
        CONF_REGION, CONF_RESOURCES
    )
from homeassistant.util import Throttle
from homeassistant.helpers.entity import Entity, generate_entity_id

from urllib.request import urlopen
import json
import xml.etree.ElementTree as ET

_LOGGER = logging.getLogger(__name__)

MIN_TIME_BETWEEN_UPDATES = timedelta(seconds=3600) 

CONCENTRATION_PARTS_PER_CUBIC_METER = "ppcm"
SENSOR_PREFIX = 'pollen'
REGIONNAME1 = 'københavn'
REGIONNAME2 = 'viborg'
SENSOR_TYPES = {
    'birk': ['Birk', 'mdi:leaf', CONCENTRATION_PARTS_PER_CUBIC_METER],
    'bynke': ['Bynke', 'mdi:leaf', CONCENTRATION_PARTS_PER_CUBIC_METER],
    'el': ['El', 'mdi:leaf', CONCENTRATION_PARTS_PER_CUBIC_METER],
    'elm': ['Elm', 'mdi:leaf', CONCENTRATION_PARTS_PER_CUBIC_METER],
    'græs': ['Græs', 'mdi:leaf', CONCENTRATION_PARTS_PER_CUBIC_METER],
    'hassel': ['Hassel', 'mdi:leaf', CONCENTRATION_PARTS_PER_CUBIC_METER],
    'alternaria': ['Alternaria', 'mdi:leaf', CONCENTRATION_PARTS_PER_CUBIC_METER],
    'cladosporium': ['Cladosporium', 'mdi:leaf', CONCENTRATION_PARTS_PER_CUBIC_METER],
    'forecast': ['Prognose', 'mdi:chart-line', ''],
    'polleninfo': ['Polleninfo', 'mdi:information-outline', ''],
    'lastupdate': ['Sidst opdateret','mdi:update',''],
}

ATTR_LAST_UPDATE = 'last_update'
ATTR_ATTRIBUTION = 'attribution'

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_REGION): cv.string,
    vol.Required(CONF_RESOURCES, default=[]):
        vol.All(cv.ensure_list, [vol.In(SENSOR_TYPES)]),
})

def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the sensor platform."""
    region = config.get(CONF_REGION).lower()
    try:
        data = DMIPollenData(region)
    except RunTimeError:
        _LOGGER.error("Unable to connect and fetch data from dmi.dk")
        return False

    entities = []

    for resource in config[CONF_RESOURCES]:
        sensor_type = resource.lower()

        if region == REGIONNAME1 or region == "all":
            entities.append(DMIPollenSensor(data, sensor_type, REGIONNAME1))

        if region == REGIONNAME2 or region == "all":     
            entities.append(DMIPollenSensor(data, sensor_type, REGIONNAME2))    

    add_entities(entities)

class DMIPollenData(object):
    """Representaition of Pollen data """

    def __init__(self, region):
        """ Initialize reading """
        self._region = region
        self.regionnames = []
        self.readings = []
        self.forecasts = []
        self.copyrighttext = None
        self.polleninfo = None
        self.date_dk = None
        self.date_string = None
    
    @Throttle(MIN_TIME_BETWEEN_UPDATES)
    def update(self):
        url = 'https://www.dmi.dk/dmidk_byvejrWS/rest/texts/forecast/pollen/Danmark/'
        response = urlopen(url)
        string = response.read().decode('utf-8')
        json_obj = json.loads(string)

        root = ET.fromstring(json_obj [0]["products"]["text"])

        self.copyrighttext  = root.find('copyright').text
        self.polleninfo = root.find('info').text
        self.date_string = root.find('file_info').find('date_DK').find('date_string').text

        year = root.find('file_info').find('date_DK').find('year').text
        month = root.find('file_info').find('date_DK').find('month').text
        day = root.find('file_info').find('date_DK').find('day').text
        time = root.find('file_info').find('date_DK').find('time').text.split(':')
        self.date_dk = datetime(int(year), int(month), int(day), int(time[0]), int(time[1]), int(time[2]))

        self.regionnames.clear()
        self.readings.clear()
        self.forecasts.clear()

        for region in root.findall('region'):
            if region.find('name').text.lower() == self._region or self._region == 'all': 
                self.regionnames.append( region.find('name').text )
                self.readings.append( region.find('readings') )
                self.forecasts.append( region.find('forecast').text)
        
        _LOGGER.debug("Date_dk = %s", self.date_dk)
        _LOGGER.debug("Regionnames = %s", self.regionnames)
        _LOGGER.debug("Readings = %s", self.readings)
        _LOGGER.debug("Forecasts = %s", self.forecasts)

class DMIPollenSensor(Entity):
    """Representation of a Pollen sensor."""

    def __init__(self, data, sensor_type, region):
        """Initialize the sensor."""
        self.data = data
        self.type = sensor_type
        self.region = region
        self._name = SENSOR_TYPES[self.type][0]
        self.entity_id = generate_entity_id( ENTITY_ID_FORMAT, SENSOR_PREFIX +"_" + self.region + "_" + self.type, [] ) 
        self._unit_of_measurement = SENSOR_TYPES[self.type][2]
        self._icon = SENSOR_TYPES[self.type][1]
        self._attribution = None
        self._polleninfo = None
        self._state = None
        self._last_update = None
        self.update()

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def icon(self):
        """Icon to use in the frontend, if any."""
        return self._icon

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement of this entity, if any."""
        return self._unit_of_measurement

    @property
    def attribution(self):
        """Return the copyright text from dmi."""
        return self._attribution 

    @property
    def last_update(self):
        """Return the copyright text from dmi."""
        return self._last_update

    @property
    def device_state_attributes(self):
        """Return the state attributes."""
        return{
            ATTR_LAST_UPDATE: self._last_update,
            ATTR_ATTRIBUTION: self._attribution,
        }

    def update(self):
        '''Get the latest data and use it to update our sensor state. '''
        self.data.update()

        self._last_update = self.data.date_dk

        self._attribution = self.data.copyrighttext

        self._polleninfo = self.data.polleninfo

        for index, regionname in enumerate(self.data.regionnames):
            if regionname.lower() == self.region.lower():
                for reading in self.data.readings[index]:
                    if reading.find('name').text.lower() == self.type.lower():
                        self._state = reading.find('value').text
                        if reading.find('value').text == '-':
                            self._state = 0
                    elif self.type.lower() == "forecast":
                        self._state = self.data.forecasts[index]
                    elif self.type.lower() == "lastupdate":
                        self._state = self.data.date_string
                    elif self.type.lower() == "polleninfo":
                        self._state = self._polleninfo