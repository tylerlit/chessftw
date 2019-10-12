DROP TABLE IF EXISTS chess.image;
DROP TABLE IF EXISTS chess.piece;

CREATE TABLE IF NOT EXISTS chess.image (
	id	INT auto_increment NOT NULL,
    image	LONGBLOB NOT NULL,
    PRIMARY KEY(id)
);

CREATE TABLE IF NOT EXISTS chess.piece (
	id int auto_increment not null,
    image_id int not null,
    location_x double not null,
    location_y double not null,
    size_x double not null,
    size_y double not null,
    piece varchar(10),
    primary key(id),
    foreign key(image_id) references chess.image(id)
);
