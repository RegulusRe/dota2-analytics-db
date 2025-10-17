DELIMITER $$

CREATE PROCEDURE GetTopPlayersByKillsInTournament(
    IN tournament_id_input BIGINT,
    OUT result_count INT
)
BEGIN
    SELECT 
        p.name AS player_name,
        SUM(s.kills) AS total_kills
    FROM Statistics s
    JOIN Players p ON s.player_id = p.player_id
    JOIN Matches m ON s.match_id = m.match_id
    WHERE m.tournament_id = tournament_id_input
    GROUP BY p.player_id, p.name
    ORDER BY total_kills DESC
    LIMIT 5;

    SELECT COUNT(*) INTO result_count
    FROM (
        SELECT p.player_id
        FROM Statistics s
        JOIN Players p ON s.player_id = p.player_id
        JOIN Matches m ON s.match_id = m.match_id
        WHERE m.tournament_id = tournament_id_input
        GROUP BY p.player_id
        ORDER BY SUM(s.kills) DESC
        LIMIT 5
    ) AS subquery;
END$$

DELIMITER ;


DELIMITER $$

CREATE PROCEDURE UpdatePlayerTeamAndStats(
    IN player_id_input BIGINT,
    IN new_team_id_input BIGINT,
    OUT success BOOLEAN
)
BEGIN
    DECLARE old_team_id BIGINT DEFAULT NULL;
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        SET success = FALSE;
    END;

    START TRANSACTION;

    SELECT team_id INTO old_team_id FROM Players WHERE player_id = player_id_input;

    IF old_team_id IS NULL THEN
        SET success = FALSE;
        ROLLBACK;
    ELSE
        UPDATE Players SET team_id = new_team_id_input WHERE player_id = player_id_input;

        SET success = TRUE;
        COMMIT;
    END IF;

END$$

DELIMITER ;


DELIMITER $$

CREATE PROCEDURE ExportPlayerStatsToFile(
    IN player_id_input BIGINT,
    OUT file_path VARCHAR(255)
)
BEGIN
    DECLARE player_name VARCHAR(255);

    SELECT name INTO player_name FROM Players WHERE player_id = player_id_input;

    SET file_path = CONCAT('/tmp/', player_name, '_stats.csv');

    SELECT
        s.stat_id,
        s.match_id,
        h.name AS hero_name,
        s.kills,
        s.deaths,
        s.assists,
        s.damage
    INTO OUTFILE file_path
    FIELDS TERMINATED BY ','
    ENCLOSED BY '"'
    LINES TERMINATED BY '\n'
    FROM Statistics s
    JOIN Heroes h ON s.hero_id = h.hero_id
    WHERE s.player_id = player_id_input;

END$$

DELIMITER ;


DELIMITER $$

CREATE PROCEDURE GetMostPlayedHeroByPlayer(
    IN player_id_input BIGINT,
    OUT hero_name_output VARCHAR(255),
    OUT games_played INT
)
BEGIN
    SELECT
        h.name,
        COUNT(*) INTO hero_name_output, games_played
    FROM Statistics s
    JOIN Heroes h ON s.hero_id = h.hero_id
    WHERE s.player_id = player_id_input
    GROUP BY h.hero_id
    ORDER BY COUNT(*) DESC
    LIMIT 1;

END$$

DELIMITER ;


DELIMITER $$

CREATE PROCEDURE ReplacePlayerFromOtherTeam(
    IN sick_player_id BIGINT,
    OUT new_player_id BIGINT
)
BEGIN
    DECLARE target_team_id BIGINT;
    DECLARE replacement_id BIGINT DEFAULT NULL;
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        SET new_player_id = NULL;
    END;

    START TRANSACTION;

    SELECT team_id INTO target_team_id
    FROM Players
    WHERE player_id = sick_player_id;

    IF target_team_id IS NULL THEN
        SET new_player_id = NULL;
        ROLLBACK;
    ELSE
        SELECT player_id INTO replacement_id
        FROM Players
        WHERE team_id != target_team_id
          AND available = TRUE
        LIMIT 1;

        IF replacement_id IS NOT NULL THEN
            UPDATE Players SET available = FALSE WHERE player_id = sick_player_id;

            UPDATE Statistics
            SET player_id = replacement_id
            WHERE player_id = sick_player_id;

            SET new_player_id = replacement_id;
        ELSE
            UPDATE Players SET available = FALSE WHERE player_id = sick_player_id;
            SET new_player_id = NULL;
        END IF;

        COMMIT;
    END IF;

END$$

DELIMITER ;