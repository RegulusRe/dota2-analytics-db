DELIMITER $$
CREATE PROCEDURE `GetTopPlayersByKillsInTournament`(
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
CREATE PROCEDURE `MakePlayerAvailable`(
    IN player_id_input BIGINT
)
BEGIN
    UPDATE Players
    SET available = TRUE
    WHERE player_id = player_id_input;
END$$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE `ReplacePlayerFromOtherTeamFlexible`(
    IN sick_player_id BIGINT,
    IN replacement_player_id BIGINT,
    OUT new_player_id BIGINT,
    OUT success BOOLEAN
)
BEGIN
    DECLARE sick_team_id BIGINT;
    DECLARE sick_position VARCHAR(100);
    DECLARE found_replacement_id BIGINT DEFAULT NULL;
    DECLARE replacement_team_id BIGINT;
    DECLARE replacement_position VARCHAR(100);
    DECLARE replacement_is_available BOOLEAN DEFAULT FALSE;
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        SET new_player_id = NULL;
        SET success = 0;
    END;

    START TRANSACTION;
    SELECT team_id, position INTO sick_team_id, sick_position
    FROM Players
    WHERE player_id = sick_player_id;

    IF sick_team_id IS NULL THEN
        SET new_player_id = NULL;
        SET success = 0;
        ROLLBACK;
    ELSE
        IF replacement_player_id IS NOT NULL THEN
            SELECT team_id, position, available INTO replacement_team_id, replacement_position, replacement_is_available
            FROM Players
            WHERE player_id = replacement_player_id;

            IF replacement_team_id IS NULL OR replacement_is_available = FALSE OR replacement_team_id = sick_team_id OR replacement_position != sick_position THEN
                SET new_player_id = NULL;
                SET success = 0;
                ROLLBACK;
            ELSE
                SET found_replacement_id = replacement_player_id;
            END IF;
        ELSE
            SELECT player_id INTO found_replacement_id
            FROM Players
            WHERE team_id != sick_team_id  
              AND position = sick_position 
              AND available = TRUE
            LIMIT 1;
        END IF;

        IF found_replacement_id IS NOT NULL THEN
            UPDATE Players SET available = FALSE WHERE player_id = sick_player_id;
            UPDATE Statistics
            SET player_id = found_replacement_id
            WHERE player_id = sick_player_id;

            SET new_player_id = found_replacement_id;
            SET success = 1;
            COMMIT;
        ELSE
            UPDATE Players SET available = FALSE WHERE player_id = sick_player_id;
            SET new_player_id = NULL;
            SET success = 0;
            COMMIT; 
        END IF;

    END IF;

END$$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE `UpdatePlayerTeamAndStats`(
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
