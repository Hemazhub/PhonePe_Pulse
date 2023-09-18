create DATABASE PULSE;
USE PULSE;
create table Agg_Trans(
State varchar(255),
Year int,
Quarter int,
Transaction_type varchar(255),
Transaction_count int,
Transaction_amount float8
);
drop table agg_trans;
select * from agg_trans;
DROP database PULSE;

CREATE TABLE Agg_Users(
STATE VARCHAR(255),
YEAR int,
Quarter int,
Brand VARCHAR(255),
reg_users_count int,
Percentage DOUBLE
);
SELECT * FROM agg_users;
DROP TABLE agg_users;
CREATE TABLE Map_Trans(
                        STATE VARCHAR(255),
                        YEAR int,
                        Quarter int,
                        District VARCHAR(255),
                        Transaction_count int,
                        Transaction_amount DOUBLE
                        );
SELECT * FROM map_trans;
                        
CREATE TABLE Map_Users(
                        STATE VARCHAR(255),
                        YEAR int,
                        Quarter int,
                        District VARCHAR(255),
                        reg_users_count int,
                        AppOpens int
                        );
SELECT * FROM map_users;
                        
CREATE TABLE Top_Trans(
                        STATE VARCHAR(255),
                        YEAR int,
                        Quarter int,
                        Pincode int,
                        Transaction_count int,
                        Transaction_amount DOUBLE
                        );
SELECT * FROM top_trans;
DROP TABLE top_trans;					
CREATE TABLE Top_Users(
                        STATE VARCHAR(255),
                        YEAR int,
                        Quarter int,
                        Pincode int,
                        reg_users_count int
                        );top_trans
SELECT * FROM top_users;
