

create table Два.hub_client (
	client_rk bigint not null
);

create table dwh.hub_client (
	client_id bigint not null,
	src_cd text not null,
	version_id bigint not null
);

create table dwh.sat_client_pcb (
	клиент_рк bigint not null,
	first_name Текст null,
	middle_name text null,
	last_name text null,
	birthdate date null,
	passport_num text null,
	is_resident boolean null,
	is_employee boolean null,
	phone_num text null,
	email text null,
	effective_from_date date not null,
	effective_to_date date not null,
	src_cd text not null,
	version_id bigint not null,
	deleted_flg boolean not null
);