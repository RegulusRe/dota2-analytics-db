CREATE OR REPLACE VIEW MatchDetails AS
SELECT
    m.match_id,
    tr.name AS team_radiant_name,
    td.name AS team_dire_name,
    tw.name AS winner_team_name,
    t.name AS tournament_name,
    m.series_id
FROM Matches m
JOIN Teams tr ON m.team_radiant = tr.team_id
JOIN Teams td ON m.team_dire = td.team_id
JOIN Teams tw ON m.winner_id = tw.team_id
JOIN Tournaments t ON m.tournament_id = t.tournament_id;


CREATE OR REPLACE VIEW PlayerStats AS
SELECT
    s.stat_id,
    p.name AS player_name,
    t.name AS team_name,
    h.name AS hero_name,
    s.kills,
    s.deaths,
    s.assists,
    s.damage,
    s.roshan_kills,
    s.towers_kills,
    m.match_id
FROM Statistics s
JOIN Players p ON s.player_id = p.player_id
JOIN Teams t ON p.team_id = t.team_id
JOIN Heroes h ON s.hero_id = h.hero_id
JOIN Matches m ON s.match_id = m.match_id;


CREATE OR REPLACE VIEW SeriesDetails AS
SELECT
    se.series_id,
    t.name AS tournament_name,
    t1.name AS team1_name,
    t2.name AS team2_name,
    tw.name AS winner_name
FROM Series se
JOIN Tournaments t ON se.tournament_id = t.tournament_id
JOIN Teams t1 ON se.team1_id = t1.team_id
JOIN Teams t2 ON se.team2_id = t2.team_id
JOIN Teams tw ON se.winner_id = tw.team_id;


CREATE OR REPLACE VIEW PrizeSummary AS
SELECT
    pr.prize_id,
    t.name AS team_name,
    tn.name AS tournament_name,
    pr.place,
    pr.amount AS prize_amount
FROM Prizes pr
JOIN Teams t ON pr.team_id = t.team_id
JOIN Tournaments tn ON pr.tournament_id = tn.tournament_id;


CREATE OR REPLACE VIEW PlayerDirectory AS
SELECT
    p.player_id,
    p.name AS player_name,
    p.nickname,
    p.position,
    t.name AS team_name
FROM Players p
LEFT JOIN Teams t ON p.team_id = t.team_id;
