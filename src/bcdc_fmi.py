'''
Created on 10.05.2021
Provides the Finnish Meteorological Institute (FMI) API data of Uni of Oulu
'''
import csv
import urllib.request

import MySQLdb
import pandas as pd
import schedule

from config import CONFIG, MYSQL_CONNECTION



ILMANET_OUTPUT = CONFIG['csv']['ilmanet']



def fetch(base_url):
    """List of lines from Ilmanet"""
    api_url_fmi = base_url + '/download.php?orderId=93173&id=127&type=solar&limit=1'

    # Ilmanet responds with Content-Type: text/csv; charset=utf-8
    # the first line is a header
    return urllib.request.urlopen(api_url_fmi)


def lines(fetched):
    """Iterable list of lines from Ilmanet"""
    fmi_csv_data = fetched
    return [line.decode('utf-8').rstrip() for line in fmi_csv_data.readlines()]


def write_csv(csv_file, content):
    """Write a two dimensional list as a .csv"""
    with open(csv_file, 'w') as f:
        writer = csv.writer(f)
        writer.writerows(content)


def parse_date_and_overwrite(csv_file):
    """Work-around for splitting date_time and eliminating timezone +03"""
    # read file
    df = pd.read_csv(csv_file, index_col='forecast_time', parse_dates=['forecast_time'],
                    date_parser=lambda x: pd.to_datetime(x.rsplit('+', 1)[0]))
    # overwrite file
    df.to_csv(csv_file, sep=',')


def insert_line(conn, line):
    """Insert a forecast line to DB"""
    sql_statement = "INSERT INTO fmi_data(forecast_time ,request_id ,power_output_w, " \
        "power_output_f0_w, power_output_f10_w, power_output_f25_w," \
        "power_output_f50_w, power_output_f75_w, power_output_f90_w, " \
        "power_output_f100_w, system_temperature_c,nominal_output_efficiency, " \
        "air_temperature_c, cloud_cover_total, " \
        "cloud_cover_high, cloud_cover_medium, " \
        "cloud_cover_low, system_radiation_global_wm2, " \
        " system_radiation_direct_wm2," \
        "system_radiation_diffuse_wm2, radiation_global_wm2, "\
        " radiation_direct_wm2, radiation_diffuse_wm2 ) " \
        "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s," \
        "%s,%s)"

    cur = conn.cursor()
    cur.executemany(sql_statement, [(line['forecast_time'],
        line['request_id'], line['power_output_w'],
        line['power_output_f0_w'], line['power_output_f10_w'],
        line['power_output_f25_w'], line['power_output_f50_w'],
        line['power_output_f75_w'], line['power_output_f90_w'],
        line['power_output_f100_w'],
        line['system_temperature_c'], line['nominal_output_efficiency'],
        line['air_temperature_c'], line['cloud_cover_total'],
        line['cloud_cover_high'], line['cloud_cover_medium'],
        line['cloud_cover_low'], line['system_radiation_global_wm2'],
        line['system_radiation_direct_wm2'], line['system_radiation_diffuse_wm2'],
        line['radiation_global_wm2'], line['radiation_direct_wm2'],
        line['radiation_diffuse_wm2'])])
    conn.escape_string(sql_statement)


def insert_from_csv(conn, csv_file):
    """Insert lines from a .csv"""
    with open(csv_file) as fmi_csv_file:
        rows = csv.DictReader(fmi_csv_file, delimiter=',')
        for row in rows:
            insert_line(conn, rows)
    conn.commit()


def cleanup_repeating(conn):
    """Cleanup previously written duplicate entries from DB"""
    # The Energy Weather data api send repeating forecast data entries, delete sql statement
    # required.
    cur = conn.cursor()
    query = "DELETE n1 FROM fmi_data n1, fmi_data n2 " \
        "WHERE n1.request_id < n2.request_id AND n1.forecast_time = n2.forecast_time"
    cur.execute(query)
    conn.commit()


def job():
    """Fetch latest forecast and commit it to DB"""
    base_url = str(CONFIG['ilmanet']['url'])
    fmi_csv = csv.reader(lines(fetch(base_url)))
    write_csv(ILMANET_OUTPUT, fmi_csv)
    parse_date_and_overwrite(ILMANET_OUTPUT)

    conn = MySQLdb.connect(**MYSQL_CONNECTION, db="smartmetering")

    insert_from_csv(conn, ILMANET_OUTPUT)
    cleanup_repeating(conn)
    print('done')



if __name__ == "__main__":
    schedule.every(180).minutes.do(job)

    while True:
        schedule.run_pending()
