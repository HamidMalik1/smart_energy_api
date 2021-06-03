'''
Created on 10.05.2021
Provides the SolarEdge API data of Uni of Oulu
'''
import csv
import time
from datetime import datetime, timedelta

import MySQLdb
import pandas as pd
import requests
import solaredge
import schedule

from config import CONFIG, MYSQL_CONNECTION



POWER_OUTPUT = CONFIG['csv']['solar_edge_power']

SOLAR_EDGE_CONFIG = CONFIG['solar_edge']

api_key = SOLAR_EDGE_CONFIG['api_key']
site_id = SOLAR_EDGE_CONFIG['site_id']



def job1():


    api_url_site_overview = str(SOLAR_EDGE_CONFIG['url']) + '/site/' + site_id + \
        '/overview.json?api_key=' + api_key
    site_overview_json_data = requests.get(api_url_site_overview).json()

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
                    'lastyearenergy': lastyearenergy, 'lastmonthenergy': lastmonthenergy,
                    'lastdayenergy': lastdayenergy, 'currentpower': currentpower}


    result4 = overview.site_overview()


    conn = MySQLdb.connect(**MYSQL_CONNECTION, db="smartmetering")
    sql_statement = "INSERT INTO solaredge_overview_api(lastupdatetime, lifetimedata, " \
        "lastyearenergy, lastmonthenergy,lastdayenergy, currentpower )  VALUES (%s,%s,%s,%s,%s,%s)"
    cur = conn.cursor()
    cur.executemany(sql_statement, [(result4['lastupdatetime'], result4['lifetimedata'],
                                    result4['lastyearenergy'], result4['lastmonthenergy'],
                                    result4['lastdayenergy'], result4['currentpower'])])

    conn.escape_string(sql_statement)
    conn.commit()



#Energy and Power Production details

def job2():

    api_data = solaredge.Solaredge(api_key)

    today = datetime.today().strftime('%Y-%m-%d')

    yesterday = datetime.now() - timedelta(1)
    yesterday = datetime.strftime(yesterday, '%Y-%m-%d')

    # Edit this date range as you see fit
    # If querying at the maximum resolution of 15 minute intervals, the API is limited to queries
    # of a month at a time This script queries one day at a time, with a one-second pause per day
    # that is polite but probably not necessary

    day_list = pd.date_range(start=yesterday, end=today)
    day_list = day_list.strftime('%Y-%m-%d')

    energy_df_list = []

    for day in day_list:
        temp = api_data.get_energy_details(site_id, day + ' 00:00:00',
            day + ' 23:59:59',
            time_unit='QUARTER_OF_AN_HOUR')
        temp_df = pd.DataFrame(temp['energyDetails']['meters'][0]['values'])
        energy_df_list.append(temp_df)
        time.sleep(1)

    power_df_list = []

    for day in day_list:
        temp = api_data.get_power_details(site_id, day + ' 00:00:00', day + ' 23:59:59')
        temp_df = pd.DataFrame(temp['powerDetails']['meters'][0]['values'])
        power_df_list.append(temp_df)
        time.sleep(1)

    energy_df = pd.concat(energy_df_list)
    energy_df.columns = ['date', 'energy']
    power_df = pd.concat(power_df_list)
    power_df.columns = ['date', 'power']

    merged = pd.merge(energy_df, power_df)
    print(energy_df, power_df)

    merged.to_csv(POWER_OUTPUT, index=False)

    with open(POWER_OUTPUT) as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',')


        for row in reader:

            conn = MySQLdb.connect(**MYSQL_CONNECTION, db="smartmetering")

            sql_statement = "INSERT INTO energy_power_production(date ,energy ,power) " \
                "VALUES (%s,%s,%s)"
            cur = conn.cursor()
            cur.executemany(sql_statement, [(row['date'], row['energy'], row['power'])])

            conn.escape_string(sql_statement)
            conn.commit()

        # Add auto_increment in energy_production table to avoid repeating values.

        sql_delete_query = "DELETE n1 FROM energy_power_production n1," \
            " energy_power_production n2 " \
            "WHERE n1.ID < n2.ID AND n1.date = n2.date "
        cur.execute(sql_delete_query)
        conn.commit()
        print('number of rows deleted', cur.rowcount)

if __name__ == "__main__":
    schedule.every(5).minutes.do(job1)
    schedule.every(15).minutes.do(job2)

    while True:
        schedule.run_pending()
