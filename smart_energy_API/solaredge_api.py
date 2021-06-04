'''
Created on 10.05.2021
Provides the SolarEdge API data of Uni of Oulu
'''
import requests

from .config import CONFIG

SOLAR_EDGE_CONFIG = CONFIG['solar_edge']



API_KEY = SOLAR_EDGE_CONFIG['api_key']
SITE_ID = SOLAR_EDGE_CONFIG['site_id']



api_url_meters = str(SOLAR_EDGE_CONFIG['url']) + '/site/' + SITE_ID \
    + '/meters?&startTime=2021-05-24%2000:00:00&endTime=2021-05-24%2023:00:00&api_key=' + API_KEY

api_url_site_energy = str(SOLAR_EDGE_CONFIG['url']) + '/site/' + SITE_ID \
    + '/energy?timeUnit=QUARTER_OF_AN_HOUR' \
    + '&endDate=2021-05-24&startDate=2021-05-24&api_key=' + API_KEY

api_url_site_power = str(SOLAR_EDGE_CONFIG['url']) + '/site/' + SITE_ID \
    + '/power?startTime=2021-05-24%2000:00:00&endTime=2021-05-25%2023:00:59&api_key=' + API_KEY

api_url_site_overview = str(SOLAR_EDGE_CONFIG['url']) + '/site/' + SITE_ID \
    + '/overview.json?api_key=' + API_KEY

api_url_site_energy_details = str(SOLAR_EDGE_CONFIG['url']) + '/site/' + SITE_ID \
    + '/energyDetails?meters=PRODUCTION,CONSUMPTION' \
    + '&timeUnit=DAY&startTime=2021-05-15%2011:00:00' \
    + '&endTime=2021-05-16%2013:00:0&api_key=' + API_KEY

api_url_site_powerflow = str(SOLAR_EDGE_CONFIG['url']) + '/site/' + SITE_ID \
    + '/currentPowerFlow.json?api_key=' + API_KEY

api_url_storage = str(SOLAR_EDGE_CONFIG['url']) + '/site/' + SITE_ID \
    + '/storageData?startTime=2021-05-23%2000:00:00' \
    + '&endTime=2021-05-24%2013:00:00&api_key=' + API_KEY

api_url_env_benefits = str(SOLAR_EDGE_CONFIG['url']) + '/site/' + SITE_ID \
    + '/envBenefits?systemUnits=Imperial&api_key=' + API_KEY

api_url_inverter_details = str(SOLAR_EDGE_CONFIG['url']) + '/equipment/' \
    + SITE_ID + '/7E1605B5-4E/data?startTime=2021-05-24%2011:55:00' \
    + '&endTime=2021-05-24%2012:00:00&api_key=' + API_KEY

api_url_sensors = str(SOLAR_EDGE_CONFIG['url']) + '/site/' + SITE_ID \
    + '/sensors?startDate=2021-05-24%2011:00:00&endDate=2021-05-25%2013:00:00&api_key=' + API_KEY



class solaredgemeters():
    @staticmethod
    def meterdata():
        data = requests.get(api_url_meters).json()
        return {'meter_api': data['meterEnergyDetails']['meters']}


class siteenergy():
    @staticmethod
    def energydata():
        data = requests.get(api_url_site_energy).json()
        return {'energy_api': data['energy']['values']}


class sitepower():
    @staticmethod
    def powerdata():
        data = requests.get(api_url_site_power).json()
        return {'power_api': data['power']['values']}


class overview():
    @staticmethod
    def site_overview():
        data = requests.get(api_url_site_overview).json()
        return {
            'lastupdatetime': data['overview']['lastUpdateTime'],
            'lifetimedata': data['overview']['lifeTimeData']['energy'] / 1000,
            'lastyearenergy': data['overview']['lastYearData']['energy'] / 1000,
            'lastmonthenergy': data['overview']['lastMonthData']['energy'] / 1000,
            'lastdayenergy': data['overview']['lastDayData']['energy'] / 1000,
            'currentpower': data['overview']['currentPower']['power']
        }


class siteenergydetails():
    @staticmethod
    def energydetailsdata():
        data = requests.get(api_url_site_energy_details).json()
        return {'energy_details_api': data['energyDetails']}


class sitepowerflow():
    @staticmethod
    def powerflowdata():
        data = requests.get(api_url_site_powerflow).json()
        return {'powerflow_api': data['siteCurrentPowerFlow']}


class sitestorage():
    @staticmethod
    def storagedata():
        data = requests.get(api_url_storage).json()
        return {'storage_api': data['storageData']}


class siteenvbenefits():
    @staticmethod
    def envdata():
        data = requests.get(api_url_env_benefits).json()
        return {'envbenefits_api': data['envBenefits']}


class siteinverter():
    @staticmethod
    def inverterdata():
        data = requests.get(api_url_inverter_details).json()
        return {'inverter_api': data['data']}


class sitesensors():
    @staticmethod
    def sensordata():
        data = requests.get(api_url_sensors).json()
        return {'sensor_api': data}
