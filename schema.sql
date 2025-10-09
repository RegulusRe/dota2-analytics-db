-- Таблиця турнірів
CREATE TABLE Tournaments (
  tournament_id BIGINT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  start_date DATE,
  end_date DATE,
  winner VARCHAR(255)
);

-- Таблиця команд
CREATE TABLE Teams (
  team_id BIGINT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(255) NOT NULL UNIQUE
);

-- Таблиця гравців
CREATE TABLE Players (
  player_id BIGINT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  nickname VARCHAR(255),
  position VARCHAR(255),
  team_id BIGINT
);

-- Таблиця героїв
CREATE TABLE Heroes (
  hero_id BIGINT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(255) NOT NULL UNIQUE,
  role VARCHAR(255),
  ultimate VARCHAR(255)
);

-- Таблиця серій
CREATE TABLE Series (
  series_id BIGINT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  tournament_id BIGINT,
  team1_id BIGINT,
  team2_id BIGINT,
  winner_id BIGINT
);

-- Таблиця матчів
CREATE TABLE Matches (
  match_id BIGINT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  series_id BIGINT,
  tournament_id BIGINT,
  team_radiant BIGINT,
  team_dire BIGINT,
  winner_id BIGINT
);

-- Таблиця статистики
CREATE TABLE Statistics (
  stat_id BIGINT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  player_id BIGINT,
  match_id BIGINT,
  hero_id BIGINT,
  kills INT,
  deaths INT,
  assists INT,
  damage INT,
  roshan_kills INT,
  towers_kills INT
);

-- Таблиця призів
CREATE TABLE Prizes (
  prize_id BIGINT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  tournament_id BIGINT,
  team_id BIGINT,
  place INT,
  amount DECIMAL
);
