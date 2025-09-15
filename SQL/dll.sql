create table users(
user_id serial primary key,
user_type varchar(20) check (user_type in ('Admin','Employee')),
password varchar(50) not null
);

create table employees(
employee_id int primary key not null unique references users(user_id) on delete cascade,
name varchar(100) not null,
email varchar(100) not null unique,
phone_num varchar(20) not null unique,
job_title varchar(100),
section_name varchar(100),
role varchar(20) check (role in ('Curator','Guide'))
);

alter table employees add column image bytea;

alter table employees drop column role;

create table administrators(
admin_id int primary key not null unique references users(user_id) on delete cascade,
name varchar(100) not null,
email varchar(100) not null unique,
section_name varchar(100)
);