create table client
(
  id       SERIAL PRIMARY KEY       not null,
  name         varchar       not null,
  dateOfBirth  date,
  age             integer   ,
  uuid   varchar(40),
  height  float,
  constraint prf_name_uk unique (name)
);

grant select on table client to postgres;
ALTER TABLE public.client OWNER TO postgres;
