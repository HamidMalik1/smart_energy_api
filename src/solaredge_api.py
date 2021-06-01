'''
Created on 10.05.2021
Provides the SolarEdge API data of Uni of Oulu
'''
import requests

from config import CONFIG

SOLAR_EDGE_CONFIG = CONFIG["solar_edge"]



api_key = SOLAR_EDGE_CONFIG["api_key"]
site_id = SOLAR_EDGE_CONFIG["site_id"]


api_url_meters = 'https://monitoringapi.solaredge.com/site/' + site_id + '/meters?&startTime=2021-05-24%2000:00:00&endTime=2021-05-24%2023:00:00&api_key=' + api_key
meters_json_data = requests.get(api_url_meters).json()

api_url_site_energy = 'https://monitoringapi.solaredge.com/site/' + site_id + '/energy?timeUnit=QUARTER_OF_AN_HOUR&endDate=2021-05-24&startDate=2021-05-24&api_key=' + api_key
site_energy_json_data = requests.get(api_url_site_energy).json()

api_url_site_power = 'https://monitoringapi.solaredge.com/site/' + site_id + '/power?startTime=2021-05-24%2000:00:00&endTime=2021-05-25%2023:00:59&api_key=' + api_key
site_power_json_data = requests.get(api_url_site_power).json()

api_url_site_overview = 'https://monitoringapi.solaredge.com/site/' + site_id + '/overview.json?api_key=' + api_key
site_overview_json_data = requests.get(api_url_site_overview).json()

api_url_site_energy_details = 'https://monitoringapi.solaredge.com/site/' + site_id + '/energyDetails?meters=PRODUCTION,CONSUMPTION&timeUnit=DAY&startTime=2021-05-15%2011:00:00&endTime=2021-05-16%2013:00:0&api_key=' + api_key
site_energy_detail_json_data = requests.get(api_url_site_energy_details).json()

api_url_site_powerflow = 'https://monitoringapi.solaredge.com/site/' + site_id + '/currentPowerFlow.json?api_key=' + api_key
site_powerflow_json_data = requests.get(api_url_site_powerflow).json()

api_url_storage = 'https://monitoringapi.solaredge.com/site/' + site_id + '/storageData?startTime=2021-05-23%2000:00:00&endTime=2021-05-24%2013:00:00&api_key=' + api_key
site_storage_json_data = requests.get(api_url_storage).json()

api_url_env_benefits = ' https://monitoringapi.solaredge.com/site/' + site_id + '/envBenefits?systemUnits=Imperial&api_key=' +api_key
site_env_benefits_json_data = requests.get(api_url_env_benefits).json()

api_url_inverter_details = 'https://monitoringapi.solaredge.com/equipment/' + site_id + '/7E1605B5-4E/data?startTime=2021-05-24%2011:55:00&endTime=2021-05-24%2012:00:00&api_key=' + api_key
site_inverter_json_data = requests.get(api_url_inverter_details).json()

api_url_sensors = ' https://monitoringapi.solaredge.com/site/' + site_id + '/sensors?startDate=2021-05-24%2011:00:00&endDate=2021-05-25%2013:00:00&api_key=' + api_key
site_sensor_json_data = requests.get(api_url_sensors).json()






class solaredgemeters():
    @staticmethod
    def meterdata():
        meter_api = meters_json_data['meterEnergyDetails']['meters']

        return {'meter_api': meter_api}


result = solaredgemeters.meterdata()
print(result['meter_api'])


class siteenergy():
    @staticmethod
    def energydata():
        energy_api = site_energy_json_data['energy']['values']

        return {'energy_api': energy_api}


result2 = siteenergy.energydata()
#print(result2['energy_api'])


class sitepower():
    @staticmethod
    def powerdata():
        power_api = site_power_json_data['power']['values']

        return {'power_api': power_api}


result3 = sitepower.powerdata()
#print(result3['power_api'])


class overview():
    @staticmethod
    def site_overview():
        lastupdatetime = site_overview_json_data['overview']['lastUpdateTime']
        lifetimedata = site_overview_json_data['overview']['lifeTimeData']['energy'] / 1000
        lastyearenergy = site_overview_json_data['overview']['lastYearData']['energy'] / 1000
        lastmonthenergy = site_overview_json_data['overview']['lastMonthData']['energy'] / 1000
        lastdayenergy = site_overview_json_data['overview']['lastDayData']['energy'] / 1000
        currentpower = site_overview_json_data['overview']['currentPower']['power']
        return {'lastupdatetime': lastupdatetime, 'lifetimedata': lifetimedata,
                'lastyearenergy': lastyearenergy, 'lastmonthenergy': lastmonthenergy, 'lastdayenergy': lastdayenergy,
                'currentpower': currentpower}


result4 = overview.site_overview()
print(result4['lastyearenergy'])



class siteenergydetails():
    @staticmethod
    def energydetailsdata():
        energy_details_api = site_energy_detail_json_data['energyDetails']

        return {'energy_details_api': energy_details_api}


result5 = siteenergydetails.energydetailsdata()
#print(result5['energy_details_api'])




class sitepowerflow():
    @staticmethod
    def powerflowdata():
        powerflow_api = site_powerflow_json_data['siteCurrentPowerFlow']

        return {'powerflow_api': powerflow_api}


result6 = sitepowerflow.powerflowdata()
print(result6['powerflow_api'])



class sitestorage():
    @staticmethod
    def storagedata():
        storage_api = site_storage_json_data['storageData']

        return {'storage_api': storage_api}


result7 = sitestorage.storagedata()
print(result7['storage_api'])



class siteenvbenefits():
     @staticmethod
     def envdata():
         envbenefits_api = site_env_benefits_json_data['envBenefits']

         return {'envbenefits_api': envbenefits_api}


result8 = siteenvbenefits.envdata()
print(result8['envbenefits_api'])



class siteinverter():
    @staticmethod
    def inverterdata():
        inverter_api = site_inverter_json_data['data']

        return {'inverter_api': inverter_api}

result9 = siteinverter.inverterdata()
#print(result9['inverter_api'])


class sitesensors():
    @staticmethod
    def sensordata():
        sensor_api = site_sensor_json_data

        return {'sensor_api': sensor_api}

result10 = sitesensors.sensordata()
print(result10['sensor_api'])


