-- Таблиця турнірів
CREATE TABLE Tournaments (
  tournament_id BIGINT PRIMARY KEY AUTO_INCREMENT,
  name VARCHAR(255) NOT NULL,
  start_date DATE,
  end_date DATE,
  winner VARCHAR(255),
  CHECK (end_date IS NULL OR start_date IS NULL OR end_date >= start_date)
);

-- Таблиця команд
CREATE TABLE Teams (
  team_id BIGINT PRIMARY KEY AUTO_INCREMENT,
  name VARCHAR(255) NOT NULL UNIQUE
);

-- Таблиця гравців
CREATE TABLE Players (
  player_id BIGINT PRIMARY KEY AUTO_INCREMENT,
  name VARCHAR(255) NOT NULL,
  nickname VARCHAR(255),
  position VARCHAR(100) CHECK (position IN ('Carry', 'Mid', 'Offlane', 'Support', 'Hard Support', 'Captain')),
  team_id BIGINT,
  FOREIGN KEY (team_id) REFERENCES Teams(team_id) ON DELETE SET NULL
);

-- Таблиця героїв
CREATE TABLE Heroes (
  hero_id BIGINT PRIMARY KEY AUTO_INCREMENT,
  name VARCHAR(255) NOT NULL UNIQUE,
  role VARCHAR(100) CHECK (role IN ('Carry', 'Mid', 'Offlane', 'Support', 'Initiator', 'Disabler', 'Nuker', 'Pusher')),
  ultimate VARCHAR(255) NOT NULL
);

-- Таблиця серій
CREATE TABLE Series (
  series_id BIGINT PRIMARY KEY AUTO_INCREMENT,
  tournament_id BIGINT NOT NULL,
  team1_id BIGINT NOT NULL,
  team2_id BIGINT NOT NULL,
  winner_id BIGINT NOT NULL,
  CHECK (team1_id != team2_id),
  CHECK (winner_id = team1_id OR winner_id = team2_id),
  FOREIGN KEY (tournament_id) REFERENCES Tournaments(tournament_id) ON DELETE CASCADE,
  FOREIGN KEY (team1_id) REFERENCES Teams(team_id) ON DELETE CASCADE,
  FOREIGN KEY (team2_id) REFERENCES Teams(team_id) ON DELETE CASCADE,
  FOREIGN KEY (winner_id) REFERENCES Teams(team_id) ON DELETE CASCADE
);

-- Таблиця матчів
CREATE TABLE Matches (
  match_id BIGINT PRIMARY KEY AUTO_INCREMENT,
  series_id BIGINT NOT NULL,
  tournament_id BIGINT NOT NULL,
  team_radiant BIGINT NOT NULL,
  team_dire BIGINT NOT NULL,
  winner_id BIGINT NOT NULL,
  CHECK (team_radiant != team_dire),
  CHECK (winner_id = team_radiant OR winner_id = team_dire),
  FOREIGN KEY (series_id) REFERENCES Series(series_id) ON DELETE CASCADE,
  FOREIGN KEY (tournament_id) REFERENCES Tournaments(tournament_id) ON DELETE CASCADE,
  FOREIGN KEY (team_radiant) REFERENCES Teams(team_id) ON DELETE CASCADE,
  FOREIGN KEY (team_dire) REFERENCES Teams(team_id) ON DELETE CASCADE,
  FOREIGN KEY (winner_id) REFERENCES Teams(team_id) ON DELETE CASCADE
);

-- Таблиця статистики
CREATE TABLE Statistics (
  stat_id BIGINT PRIMARY KEY AUTO_INCREMENT,
  player_id BIGINT NOT NULL,
  match_id BIGINT NOT NULL,
  hero_id BIGINT NOT NULL,
  kills INT DEFAULT 0 CHECK (kills >= 0),
  deaths INT DEFAULT 0 CHECK (deaths >= 0),
  assists INT DEFAULT 0 CHECK (assists >= 0),
  damage INT DEFAULT 0 CHECK (damage >= 0),
  roshan_kills INT DEFAULT 0 CHECK (roshan_kills >= 0),
  towers_kills INT DEFAULT 0 CHECK (towers_kills >= 0),
  FOREIGN KEY (player_id) REFERENCES Players(player_id) ON DELETE CASCADE,
  FOREIGN KEY (match_id) REFERENCES Matches(match_id) ON DELETE CASCADE,
  FOREIGN KEY (hero_id) REFERENCES Heroes(hero_id) ON DELETE CASCADE,
  UNIQUE (player_id, match_id)
);

-- Таблиця призів
CREATE TABLE Prizes (
  prize_id BIGINT PRIMARY KEY AUTO_INCREMENT,
  tournament_id BIGINT NOT NULL,
  team_id BIGINT NOT NULL,
  place INT NOT NULL CHECK (place >= 1 AND place <= 16),
  amount DECIMAL(15,2) NOT NULL CHECK (amount >= 0),
  FOREIGN KEY (tournament_id) REFERENCES Tournaments(tournament_id) ON DELETE CASCADE,
  FOREIGN KEY (team_id) REFERENCES Teams(team_id) ON DELETE CASCADE,
  UNIQUE (tournament_id, place),
  UNIQUE (tournament_id, team_id)
);
