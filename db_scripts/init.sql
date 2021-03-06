CREATE DATABASE CricketDb;
use CricketDb;

CREATE TABLE IF NOT EXISTS odi_ball_by_ball (
`id`	INTEGER NOT NULL AUTO_INCREMENT,
`cricsheet_id` INTEGER NOT NULL,
`venue`	TEXT,
`year`	INTEGER,
`ball_team`	TEXT,
`bat_team`	TEXT,
`ball_number`	TEXT,
`bowler_name`	TEXT,
`batsman_name`	TEXT,
`non_striker_name`	TEXT,
`runs_batsman`	INTEGER,
`runs_extras`	INTEGER,
`runs_total`	INTEGER,
PRIMARY KEY(`id`)
);