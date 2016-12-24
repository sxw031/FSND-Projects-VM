-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.
DROP DATABASE IF EXISTS tournament;
CREATE DATABASE tournament;
\c tournament

CREATE TABLE players (  id SERIAL PRIMARY KEY,
                    	name varchar(255) NOT NULL);

CREATE TABLE matches (  id SERIAL PRIMARY KEY,
						winner INTEGER REFERENCES players (id),
						loser INTEGER REFERENCES players (id));

CREATE VIEW total_wins As 
	SELECT players.id AS player_id, players.name AS player_name, 
	(SELECT count(*) FROM matches WHERE players.id = matches.winner) AS wins,
	(SELECT count(*) FROM matches WHERE players.id in (winner, loser)) AS played_matches
	FROM players
	GROUP BY players.id
	ORDER BY wins DESC;