create table if not exists genre (
	id serial primary key,
	name varchar(60) not null unique
);

create table if not exists artist (
	id serial primary key,
	name varchar(60) not null
);


create table if not exists artist_genre(
	id serial primary key,
	genre_id integer not null references genre(id),
	artist_id integer not null references artist(id)
);

create table if not exists album (
	id serial primary key,
	name varchar(60) not null,
	releaseDate date not null
);

create table if not exists album_artist (
	id  serial primary key,
	artist_id integer not null references artist(id),
	album_id integer not null references album(id)
);

create table if not exists track (
	id serial primary key,
	name varchar(60) not null,
	trackLength numeric(3,2) not null,
	album_id integer references album(id) 
);

create table if not exists collections(
	id serial primary key,
	name varchar(60) not null,
	release_year date  not null
);

create table if not exists collections_album_track(
	id serial primary key,
	collections_id integer not null references collections(id),
	album_id integer not null references album(id),
	track_id integer not null references track(id)
);
