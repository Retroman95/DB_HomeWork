create table if not exists artist_list(
	id serial primary key,
	artist_name varchar(255) not null,
	alias varchar(80) not null
);
	
create table if not exists artist_in_genre(
	id serial primary key,
	artist_id integer not null references artist_list(id),
	genre_id integer not null references Genre_List(id)
);
	
create table if not exists Genre_list(
	id serial primary key, 
	genre_name  varchar(80)
);
	
create table if not exists album_List (
	id serial primary key,
	album_name varchar(80) not null,
	release_date varchar(80) not null
);
	
create table if not exists artist_album(
	id  serial primary key,
	artist_id integer not null references artist_list(id),
	album_id integer not null references album_List(id)
);
	
create table if not exists collection_List(
	id serial primary key,
	collection_name varchar(60) not null,
	release_date date not null
);
	
create table if not exists collection_track(
	collection_id integer not null references collection_list(id),
	track_id integer not null references Track_List(id)
	constraint pk__ primary key (collection_id, track_id)
);	
	
create table if not exists track_List (
	id serial primary key,
	album_id integer references album_List(id),
	track_name varchar(80) not null,
	track_time time not null)
	;
