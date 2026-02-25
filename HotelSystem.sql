create database Hotel_Management_System;
use Hotel_Management_System;

create table login(
name varchar(50),
password varchar(50)
);

insert into login values
("name","12345");

create table register(
id int auto_increment primary key,
FirstName varchar(50),
LastName varchar(50),
Email varchar(50),
PhoneNumber bigint unique,
password varchar(50),
confirmPassword varchar(50)
);

select * from register;

create table forgot(
id int auto_increment primary key,
newPassword varchar(50),
ConfirmPassword varchar(50)
);

select * from forgot;
