create table if not exists artist_list(
	id serial primary key,
	artist_name varchar(255) not null,
	alias varchar(80) not null);
	
create table if not exists artist_in_genre(
	id serial primary key,
	artist_id integer not null references artist_list(id),
	genre_id integer not null references Genre_List(id));
	
create table if not exists Genre_list(
	id serial primary key, 
	genre_name  varchar(80) not null reference artist_in_genre(genre_id);
							
create table if not exists artist_album(
	id  serial primary key,
	artist_id integer not null references artist_list(id),
	album_id integer not null references album_List(id));
	
create table if not exists album_List (
	id serial primary key,
	album_name varchar(80) not null,
	release_date varchar(80) not null);
	
create table if not exists Track_List (
	id serial primary key references collection_album_track(track_id),
	album_id integer references album_List(id)
	track_name varchar(80) not null,
	track_time varchar(80) not null);
		
create table if not exists collection_List(
	id serial primary key,
	collection_name varchar(60) not null,
	release_date  not null);
							
create table if not exists collection_album_track(
	id serial primary key,
	collection_id integer not null references collection_list(id),
	track_id integer not null references Track_List(id));
