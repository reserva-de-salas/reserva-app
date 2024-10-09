create database reservaSalas;

use reservaSalas;

create table usuario (
	id int primary key auto_increment,
    nome varchar (100) not null,
    email varchar (255) not null,
    salt varchar (32) not null,
    hash_senha varchar (64) not null
);

create table salas (
	id int primary key auto_increment,
    tipo varchar (50) not null,
    descricao varchar (150),
    capacidade smallint not null,
    ativa boolean not null
);

create table reservas (
	id int primary key auto_increment,
    id_sala int,
    inicio datetime,
    fim datetime,
	foreign key(id_sala) references salas(id)
);