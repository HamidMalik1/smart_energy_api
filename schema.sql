
CREATE TABLE fmi_data(forecast_time TIMESTAMP, request_id int, power_output_w varchar(255), power_output_f0_w varchar(255), "
             "power_output_f10_w varchar(255), power_output_f25_w varchar(255), power_output_f50_w varchar(255), power_output_f75_w varchar(255), "
             "power_output_f90_w varchar(255), power_output_f100_w varchar(255), system_temperature_c varchar(255), nominal_output_efficiency varchar(255), "
             "air_temperature_c varchar(255), cloud_cover_total varchar(255),cloud_cover_high varchar(255), cloud_cover_medium varchar(255), cloud_cover_low varchar(255)," 
             "system_radiation_global_wm2 varchar(255), system_radiation_direct_wm2 varchar(255), system_radiation_diffuse_wm2 varchar(255), )



CREATE TABLE energy_power_production (ID int , date TIMESTAMP, energy varchar(255), power varchar(255) ) #ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE


CREATE TABLE solaredge_overview_api (lastupdatetime varchar(255), lifetimedata float, lastyearenergy float, lastmonthenergy float, lastdayenergy float, currentpower float)

