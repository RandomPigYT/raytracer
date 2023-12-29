create user if not exists 'raytracerBot'@'localhost' identified by 'password';
GRANT ALL PRIVILEGES ON *.* TO 'raytracerBot'@'localhost' WITH GRANT OPTION;
FLUSH PRIVILEGES;
create database if not exists raytracer;
use raytracer;
create table if not exists scenes(name varchar(100) primary key);