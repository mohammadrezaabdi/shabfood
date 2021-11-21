---------------------------INITIALIZATION--------------------------
drop schema if exists public cascade;
create schema if not exists public;
create extension if not exists "uuid-ossp";
create extension if not exists "pgcrypto";

------------------------------DOMAINS------------------------------

drop domain if exists global_name cascade;
create domain global_name as text
    check ( value ~ '^[A-Za-z0-9]+(?:[ _-][A-Za-z0-9]+)*$');

drop domain if exists phone_number cascade;
create domain phone_number as text
    check ( value ~ '^[+]*[(]{0,1}[0-9]{1,4}[)]{0,1}[-\s\./0-9]*$' );

drop domain if exists address cascade;
create domain address as text
    check ( value ~ '[A-Za-z0-9\s\.]*');

drop domain if exists email_address cascade;
create domain email_address as text
    check ( value ~
            '^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$' );

-------------------------------TABLES-------------------------------

drop table if exists Restaurant cascade;
create table if not exists Restaurant
(
    id       email_address not null,
    password varchar(72)   not null,
    name     global_name   not null,
    address  address       not null,
    primary key (id)
);

drop table if exists Customer cascade;
create table if not exists Customer
(
    id       phone_number not null,
    password varchar(72)  not null,
    address  address      not null,
    primary key (id)
);

drop table if exists Deliverer cascade;
create table if not exists Deliverer
(
    id       phone_number not null,
    password varchar(72)  not null,
    status   smallint     not null,
    primary key (id)
);

drop table if exists Food cascade;
create table if not exists Food
(
    id     uuid        not null,
    name   global_name not null,
    price  int         not null,
    status smallint    not null,
    primary key (id)
);

drop table if exists Food_order cascade;
create table if not exists Food_Order
(
    id            uuid          not null,
    customer_id   phone_number  not null,
    restaurant_id email_address not null,
    deliverer_id  phone_number,
    timestamp     char(19)      not null,
    status        smallint      not null,
    primary key (id),
    foreign key (customer_id) references Customer (id) on update cascade on delete cascade,
    foreign key (restaurant_id) references Restaurant (id) on update cascade on delete cascade,
    foreign key (deliverer_id) references Deliverer (id) on update cascade on delete cascade
);

drop table if exists Menu cascade;
create table if not exists Menu
(
    food_id       uuid          not null,
    restaurant_id email_address not null,
    primary key (food_id, restaurant_id),
    foreign key (food_id) references Food (id) on update cascade on delete cascade,
    foreign key (restaurant_id) references Restaurant (id) on update cascade on delete cascade
);

drop table if exists Order_items cascade;
create table if not exists Order_items
(
    order_id uuid     not null,
    food_id  uuid     not null,
    quantity smallint not null,
    primary key (food_id, order_id),
    foreign key (food_id) references Food (id) on update cascade on delete cascade,
    foreign key (order_id) references Food_Order (id) on update cascade on delete cascade
);

--------------------------------TRIGGER-FUNCTIONS-----------------------------------------

create or replace function password_encryptor() returns trigger as
$$
begin
    new.password := crypt(new.password, gen_salt('bf'));
    return new;
end
$$ language plpgsql;

--------------------------------------TRIGGERS----------------------------------------------

drop trigger if exists customer_password_encryptor on Customer cascade;
create trigger customer_password_encryptor
    before insert
    on Customer
    for each row
execute procedure password_encryptor();

drop trigger if exists customer_password_updater on Customer cascade;
create trigger customer_password_updater
    before update of password
    on Customer
    for each row
execute procedure password_encryptor();

drop trigger if exists restaurant_password_encryptor on Restaurant cascade;
create trigger restaurant_password_encryptor
    before insert
    on Restaurant
    for each row
execute procedure password_encryptor();

drop trigger if exists restaurant_password_updater on Restaurant cascade;
create trigger restaurant_password_updater
    before update of password
    on Restaurant
    for each row
execute procedure password_encryptor();

drop trigger if exists deliverer_password_encryptor on Deliverer cascade;
create trigger deliverer_password_encryptor
    before insert
    on Deliverer
    for each row
execute procedure password_encryptor();

drop trigger if exists deliverer_password_updater on Deliverer cascade;
create trigger deliverer_password_updater
    before update of password
    on Deliverer
    for each row
execute procedure password_encryptor();

----------------------------------------------------------------------------------------------
