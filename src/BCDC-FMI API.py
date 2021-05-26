'''
Created on 10.05.2021
Provides the Finnish Meteorological Institute (FMI) API data of Uni of Oulu
'''

import urllib.request
import csv
import pandas as pd
import MySQLdb



#Database connection settings
conn = MySQLdb.connect(host="localhost", port=3306, user="root", passwd="5gtnoulu", db="smartmetering")


api_url_fmi = 'http://ilmanet.fi/download.php?orderId=93173&id=127&type=solar&limit=1'
fmi_csv_data = urllib.request.urlopen(api_url_fmi)
lines = [l.decode('utf-8') for l in fmi_csv_data.readlines()]
fmi_csv = csv.reader(lines)

with open('C:/Users/hamalik/Desktop/pythonProject/Solaredge-FMI/fmi_api_data.csv', 'w') as f:
    for row in fmi_csv:
        for x in row:
            f.write(str(x) + ',')
        f.write('\n')






#This is for splitting date_time and eliminating timezone +03

file_name = 'C:/Users/hamalik/Desktop/pythonProject/Solaredge-FMI/fmi_api_data.csv'
df = pd.read_csv(file_name, index_col='forecast_time', parse_dates=['forecast_time'],
                 date_parser=lambda x: pd.to_datetime(x.rsplit('+', 1)[0]))

df.to_csv(file_name, sep=',')


with open ('C:/Users/hamalik/Desktop/pythonProject/Solaredge-FMI/fmi_api_data.csv') as fmi_csv_file:
    reader = csv.DictReader(fmi_csv_file, delimiter=',')
    for row in reader:
        sql_statement = "INSERT INTO fmi_data(forecast_time ,request_id ,power_output_w, " \
                        "power_output_f0_w, power_output_f10_w, power_output_f25_w," \
                        "power_output_f50_w, power_output_f75_w, power_output_f90_w, " \
                        "power_output_f100_w, system_temperature_c,nominal_output_efficiency," \
                        " air_temperature_c, cloud_cover_total, cloud_cover_high, cloud_cover_medium, " \
                        "cloud_cover_low, system_radiation_global_wm2, system_radiation_direct_wm2," \
                        "system_radiation_diffuse_wm2, radiation_global_wm2, radiation_direct_wm2," \
                        " radiation_diffuse_wm2  ) " \
                        "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

        cur = conn.cursor()
        cur.executemany(sql_statement, [(row['forecast_time'], row['request_id'], row['power_output_w'],
                                         row['power_output_f0_w'], row['power_output_f10_w'],
                                         row['power_output_f25_w'], row['power_output_f50_w'],
                                         row['power_output_f75_w'], row['power_output_f90_w'],
                                         row['power_output_f100_w'],
                                         row['system_temperature_c'], row['nominal_output_efficiency'],
                                         row['air_temperature_c'], row['cloud_cover_total'],
                                         row['cloud_cover_high'], row['cloud_cover_medium'],
                                         row['cloud_cover_low'], row['system_radiation_global_wm2'],
                                         row['system_radiation_direct_wm2'], row['system_radiation_diffuse_wm2'],
                                         row['radiation_global_wm2'], row['radiation_direct_wm2'],
                                         row['radiation_diffuse_wm2'])])
        conn.escape_string(sql_statement)
conn.commit()



#The Energy Weather data api send repeating forecast data entries, delete sql statement required.

sql_delete_repeating_entries_query = "DELETE n1 FROM fmi_data n1, " \
                        "fmi_data n2 WHERE n1.request_id < n2.request_id AND n1.forecast_time = n2.forecast_time "
cur.execute(sql_delete_repeating_entries_query)
conn.commit()
