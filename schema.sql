CREATE DATABASE smartmetering;

USE smartmetering;

CREATE TABLE fmi_data(
    id int NOT NULL AUTO_INCREMENT,
    forecast_time timestamp UNIQUE NOT NULL,
    request_id int NOT NULL,
    power_output_w varchar(255),
    power_output_f0_w varchar(255),
    power_output_f10_w varchar(255),
    power_output_f25_w varchar(255),
    power_output_f50_w varchar(255),
    power_output_f75_w varchar(255),
    power_output_f90_w varchar(255),
    power_output_f100_w varchar(255),
    system_temperature_c varchar(255),
    nominal_output_efficiency varchar(255),
    air_temperature_c varchar(255),
    cloud_cover_total varchar(255),
    cloud_cover_high varchar(255),
    cloud_cover_medium varchar(255),
    cloud_cover_low varchar(255),
    system_radiation_global_wm2 varchar(255),
    system_radiation_direct_wm2 varchar(255),
    system_radiation_diffuse_wm2 varchar(255),
    radiation_global_wm2 varchar(255),
    radiation_direct_wm2 varchar(255),
    radiation_diffuse_wm2 varchar(255),
    PRIMARY KEY (id)
);


CREATE TABLE energy_power_production (
    id int NOT NULL AUTO_INCREMENT,
    date timestamp UNIQUE NOT NULL,
    energy varchar(255),
    power varchar(255),
    PRIMARY KEY (id)
);


CREATE TABLE solaredge_overview_api (
    id int NOT NULL AUTO_INCREMENT,
    lastupdatetime varchar(255),
    lifetimedata float,
    lastyearenergy float,
    lastmonthenergy float,
    lastdayenergy float,
    currentpower float,
    PRIMARY KEY (id)
);
