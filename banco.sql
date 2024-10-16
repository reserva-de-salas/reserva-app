-- create database if not exists reservasalas;
-- use reservaSalas;

create table if not exists usuario (
	id int primary key auto_increment,
    nome varchar (100) not null,
    email varchar (255) not null,
    salt varchar (32) not null,
    hash_senha varchar (64) not null
);

create table if not exists salas (
	id int primary key auto_increment,
    tipo varchar (50) not null,
    capacidade smallint not null,
    descricao varchar (150),
    ativa boolean not null
);

create table if not exists reservas (
	id int primary key auto_increment,
    id_sala int,
    inicio datetime,
    fim datetime,
	foreign key(id_sala) references salas(id) on delete cascade
);