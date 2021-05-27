'''
Created on 10.05.2021
Provides the SolarEdge API data of Uni of Oulu
'''


import solaredge
import schedule
import requests
import MySQLdb
from datetime import datetime, timedelta
import csv
import pandas as pd
import time





today = datetime.today().strftime('%Y-%m-%d')
print(today)
yesterday = datetime.now() - timedelta(1)
yesterday = datetime.strftime(yesterday, '%Y-%m-%d')
print(yesterday)



api_key = 'I8AZZW5B2XGFNM3WSJ8IDA0441Z9TQ9V'
site_id = '1703225'


def job1():


    api_url_site_overview = 'https://monitoringapi.solaredge.com/site/' + site_id + '/overview.json?api_key=' + api_key
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
                    'lastyearenergy': lastyearenergy, 'lastmonthenergy': lastmonthenergy, 'lastdayenergy': lastdayenergy,
                    'currentpower': currentpower}


    result4 = overview.site_overview()


    conn = MySQLdb.connect(host="localhost", port=3306, user="root", passwd="5gtnoulu", db="smartmetering")
    sql_statement = "INSERT INTO solaredge_overview_api(lastupdatetime ,lifetimedata, lastyearenergy,lastmonthenergy,lastdayenergy, currentpower )  VALUES (%s,%s,%s,%s,%s,%s)"
    cur = conn.cursor()
    cur.executemany(sql_statement, [(result4['lastupdatetime'], result4['lifetimedata'], result4['lastyearenergy'],
                                    result4['lastmonthenergy'], result4['lastdayenergy'], result4['currentpower'])])

    conn.escape_string(sql_statement)
    conn.commit()

    return



#Energy and Power Production details

def job2():

    api_data = solaredge.Solaredge("I8AZZW5B2XGFNM3WSJ8IDA0441Z9TQ9V")
    conn = MySQLdb.connect(host="localhost", port=3306, user="root", passwd="5gtnoulu", db="smartmetering")

    # Edit this date range as you see fit
    # If querying at the maximum resolution of 15 minute intervals, the API is limited to queries of a month at a time
    # This script queries one day at a time, with a one-second pause per day that is polite but probably not necessary

    day_list = pd.date_range(start=yesterday, end=today)
    day_list = day_list.strftime('%Y-%m-%d')

    energy_df_list = []

    for day in day_list:
        temp = api_data.get_energy_details(site_id, day + ' 00:00:00', day + ' 23:59:59', time_unit='QUARTER_OF_AN_HOUR')
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

    merged.to_csv("C:/Users/hamalik/Desktop/pythonProject/Solaredge-FMI/energy_power_production.csv", index=False)

    with open('C:/Users/hamalik/Desktop/pythonProject/Solaredge-FMI/energy_power_production.csv') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',')


        for row in reader:

            sql_statement = "INSERT INTO energy_power_production(date ,energy ,power)  VALUES (%s,%s,%s)"
            cur = conn.cursor()
            cur.executemany(sql_statement, [(row['date'], row['energy'], row['power'])])

            conn.escape_string(sql_statement)
            conn.commit()

        sql_Delete_query = """DELETE n1 FROM energy_power_production n1, energy_power_production n2 WHERE n1.ID < n2.ID AND n1.date = n2.date """
        cur.execute(sql_Delete_query)
        conn.commit()
        print('number of rows deleted', cur.rowcount)

    return


schedule.every(5).minutes.do(job1)
schedule.every(15).minutes.do(job2)

while True:
    schedule.run_pending()


