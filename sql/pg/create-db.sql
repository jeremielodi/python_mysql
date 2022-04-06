--\encoding utf-8
/*
DROP role if exists fac_db_user;
create role fac_db_user;
create role schema_owner login password 'HyzzpU81Ai';

-- Utilisateur qui doit être utilisé par l'application pour se connecter à la BdD.
create role fac_app login password 'JGcFvd54Di8D' in role fac_db_user;
create database factures01 with owner = schema_owner encoding = 'UTF8';

create extension unaccent;

revoke all on schema public from public;
grant all on schema public to schema_owner;
grant usage on schema public to fac_db_user;
*/

