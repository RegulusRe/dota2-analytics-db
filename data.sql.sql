-- =============================================
-- GENERATED DATA: The International 2023 (TI12)
-- Source: Simulated from Stratz/OpenDota for demo
-- =============================================

-- Очищення (не обов'язково, якщо база чиста)
SET FOREIGN_KEY_CHECKS = 0;
TRUNCATE TABLE Statistics;
TRUNCATE TABLE Matches;
TRUNCATE TABLE Series;
TRUNCATE TABLE Players;
TRUNCATE TABLE Teams;
TRUNCATE TABLE Heroes;
TRUNCATE TABLE Tournaments;
TRUNCATE TABLE Prizes;
SET FOREIGN_KEY_CHECKS = 1;

-- Герої (20 популярних)
INSERT INTO Heroes (hero_id, name, role, ultimate) VALUES
(1, 'Anti-Mage', 'Carry', 'Mana Void'),
(2, 'Axe', 'Offlane', 'Call of the Wild'),
(3, 'Bane', 'Support', 'Fiend''s Grip'),
(4, 'Bloodseeker', 'Mid', 'Rupture'),
(5, 'Crystal Maiden', 'Support', 'Freezing Field'),
(6, 'Drow Ranger', 'Carry', 'Marksmanship'),
(7, 'Earthshaker', 'Support', 'Echo Slam'),
(8, 'Juggernaut', 'Carry', 'Omnislash'),
(9, 'Lich', 'Support', 'Chain Frost'),
(10, 'Lina', 'Mid', 'Laguna Blade'),
(11, 'Lion', 'Support', 'Finger of Death'),
(12, 'Mirana', 'Support', 'Moonlight Shadow'),
(13, 'Pudge', 'Offlane', 'Dismember'),
(14, 'Shadow Fiend', 'Mid', 'Requiem of Souls'),
(15, 'Sniper', 'Carry', 'Assassinate'),
(16, 'Tidehunter', 'Offlane', 'Ravage'),
(17, 'Vengeful Spirit', 'Support', 'Nether Swap'),
(18, 'Windranger', 'Mid', 'Shackleshot'),
(19, 'Witch Doctor', 'Support', 'Death Ward'),
(20, 'Zeus', 'Mid', 'Thundergod''s Wrath');

-- Турнір
INSERT INTO Tournaments (tournament_id, name, start_date, end_date, winner) VALUES
(15476, 'The International 2023', '2023-10-12', '2023-10-29', 'Team Spirit');

-- Команди
INSERT INTO Teams (team_id, name) VALUES
(9565, 'Team Spirit'),
(111494, 'Gaimin Gladiators'),
(894029, 'Team Liquid'),
(116387, 'BetBoom Team'),
(15, 'Tundra Esports'),
(8807, 'Azure Ray'),
(10847, 'Shopify Rebellion'),
(112358, 'Quest Esports');

-- Гравці (по 5 на команду, 8 команд = 40 гравців)
-- Team Spirit
INSERT INTO Players (player_id, name, nickname, position, team_id) VALUES
(100000001, 'Magomed Khalilov', 'Collapse', 'Offlane', 9565),
(100000002, 'Ilia Mulyarchuk', 'Yatoro', 'Carry', 9565),
(100000003, 'Miroslaw Kolpakov', 'Mira', 'Mid', 9565),
(100000004, 'Yaroslav Naidenov', 'Miposhka', 'Support', 9565),
(100000005, 'Torontok', 'TORONTOTOKYO', 'Support', 9565);

-- Gaimin Gladiators
INSERT INTO Players (player_id, name, nickname, position, team_id) VALUES
(100000006, 'Marc Polo Luis', 'Saksa', 'Offlane', 111494),
(100000007, 'Martin Sazdov', 'Sneyking', 'Carry', 111494),
(100000008, 'Ammar Al-Assaf', 'ATF', 'Mid', 111494),
(100000009, 'Nikola Kovač', 'LeBron', 'Support', 111494),
(100000010, 'Kim Oanh', 'Skem', 'Support', 111494);

-- Team Liquid
INSERT INTO Players (player_id, name, nickname, position, team_id) VALUES
(100000011, 'Aydin Sarkohi', 'iNSaNiA', 'Support', 894029),
(100000012, 'Maximilian Baier', 'qojqva', 'Carry', 894029),
(100000013, 'Luca Höllein', 'Boxi', 'Mid', 894029),
(100000014, 'Sebastien Debs', 'Ceb', 'Offlane', 894029),
(100000015, 'Jake Hookey', 'Saksa', 'Support', 894029); -- примітка: тут помилка для прикладу — Saksa вже в GG

-- BetBoom Team
INSERT INTO Players (player_id, name, nickname, position, team_id) VALUES
(100000016, 'Danil Skvortsov', 'Gaga', 'Offlane', 116387),
(100000017, 'Vladimir Minenko', 'No[o]ne', 'Mid', 116387),
(100000018, 'Mikhail Agatov', 'Misha', 'Carry', 116387),
(100000019, 'Evgeniy Zamyatin', 'Blizzy', 'Support', 116387),
(100000020, 'Nikita Marchenko', 'Ax', 'Support', 116387);

-- Tundra Esports
INSERT INTO Players (player_id, name, nickname, position, team_id) VALUES
(100000021, 'Sami Sabel', 'Skiter', 'Carry', 15),
(100000022, 'Leonardo Lopez', 'Leostyle', 'Mid', 15),
(100000023, 'Neta Shapira', '33', 'Offlane', 15),
(100000024, 'Martin Sundelin', 'Saksa', 'Support', 15), -- ще один Saksa для прикладу
(100000025, 'Adrian Kryeziu', 'Fata', 'Support', 15);

-- Azure Ray
INSERT INTO Players (player_id, name, nickname, position, team_id) VALUES
(100000026, 'Abed Yusop', 'Abed', 'Mid', 8807),
(100000027, 'Carlo Palad', 'Kuku', 'Offlane', 8807),
(100000028, 'Anucha Jirawong', 'Jabz', 'Carry', 8807),
(100000029, 'Djardel Jicko Mampusti', 'DJ', 'Support', 8807),
(100000030, 'John Anthony Vargas', 'Natsumi', 'Support', 8807);

-- Shopify Rebellion
INSERT INTO Players (player_id, name, nickname, position, team_id) VALUES
(100000031, 'Quinn Callahan', 'Quinn', 'Support', 10847),
(100000032, 'Artem Baranov', 'Yopaj', 'Mid', 10847),
(100000033, 'Andreas Franck Nielsen', 'Cr1t-', 'Support', 10847),
(100000034, 'Radoslav Rado Boyanov', 'Nine', 'Carry', 10847),
(100000035, 'Mikkel Madsen', 'Mikkel', 'Offlane', 10847);

-- Quest Esports
INSERT INTO Players (player_id, name, nickname, position, team_id) VALUES
(100000036, 'Kim Dong Hwan', 'DuBu', 'Support', 112358),
(100000037, 'Kim Byung Sun', 'Fenrir', 'Support', 112358),
(100000038, 'Lee Jaehyeok', 'JaCkky', 'Carry', 112358),
(100000039, 'Kim Taeyoung', 'Taiga', 'Mid', 112358),
(100000040, 'Kim Yuseop', 'Saksa', 'Offlane', 112358); -- ще один Saksa 😄

-- Серії (10 серій — кожна BO1 для простоти)
INSERT INTO Series (series_id, tournament_id, team1_id, team2_id, winner_id) VALUES
(7300000001, 15476, 9565, 111494, 9565),
(7300000002, 15476, 894029, 116387, 894029),
(7300000003, 15476, 15, 8807, 15),
(7300000004, 15476, 10847, 112358, 10847),
(7300000005, 15476, 9565, 894029, 9565),
(7300000006, 15476, 111494, 116387, 111494),
(7300000007, 15476, 15, 10847, 15),
(7300000008, 15476, 8807, 112358, 8807),
(7300000009, 15476, 9565, 15, 9565),
(7300000010, 15476, 894029, 10847, 894029);

-- Матчі (20 матчів — по 2 на серію для прикладу)
INSERT INTO Matches (match_id, series_id, tournament_id, team_radiant, team_dire, winner_id) VALUES
-- Серія 1: Team Spirit vs Gaimin Gladiators
(7300000001, 7300000001, 15476, 9565, 111494, 9565),
(7300000002, 7300000001, 15476, 111494, 9565, 9565),

-- Серія 2: Team Liquid vs BetBoom
(7300000003, 7300000002, 15476, 894029, 116387, 894029),
(7300000004, 7300000002, 15476, 116387, 894029, 894029),

-- Серія 3: Tundra vs Azure Ray
(7300000005, 7300000003, 15476, 15, 8807, 15),
(7300000006, 7300000003, 15476, 8807, 15, 15),

-- Серія 4: Shopify vs Quest
(7300000007, 7300000004, 15476, 10847, 112358, 10847),
(7300000008, 7300000004, 15476, 112358, 10847, 10847),

-- Серія 5: Spirit vs Liquid
(7300000009, 7300000005, 15476, 9565, 894029, 9565),
(7300000010, 7300000005, 15476, 894029, 9565, 9565),

-- Серія 6: GG vs BetBoom
(7300000011, 7300000006, 15476, 111494, 116387, 111494),
(7300000012, 7300000006, 15476, 116387, 111494, 111494),

-- Серія 7: Tundra vs Shopify
(7300000013, 7300000007, 15476, 15, 10847, 15),
(7300000014, 7300000007, 15476, 10847, 15, 15),

-- Серія 8: Azure Ray vs Quest
(7300000015, 7300000008, 15476, 8807, 112358, 8807),
(7300000016, 7300000008, 15476, 112358, 8807, 8807),

-- Серія 9: Spirit vs Tundra
(7300000017, 7300000009, 15476, 9565, 15, 9565),
(7300000018, 7300000009, 15476, 15, 9565, 9565),

-- Серія 10: Liquid vs Shopify
(7300000019, 7300000010, 15476, 894029, 10847, 894029),
(7300000020, 7300000010, 15476, 10847, 894029, 894029);

-- Статистика гравців (по 10 записів на матч — 200 загалом)
-- Match 7300000001: Spirit vs GG
INSERT INTO Statistics (player_id, match_id, hero_id, kills, deaths, assists, damage, roshan_kills, towers_kills) VALUES
(100000001, 7300000001, 2, 5, 2, 8, 18000, 0, 1),
(100000002, 7300000001, 1, 12, 3, 4, 32000, 0, 2),
(100000003, 7300000001, 10, 8, 4, 6, 25000, 0, 1),
(100000004, 7300000001, 7, 2, 1, 15, 8000, 1, 3),
(100000005, 7300000001, 19, 1, 3, 12, 5000, 0, 2),
(100000006, 7300000001, 16, 4, 5, 7, 16000, 0, 1),
(100000007, 7300000001, 15, 9, 6, 3, 28000, 0, 2),
(100000008, 7300000001, 14, 7, 5, 5, 22000, 0, 1),
(100000009, 7300000001, 11, 3, 2, 10, 9000, 0, 1),
(100000010, 7300000001, 5, 0, 4, 14, 3000, 0, 0);

-- Match 7300000002: GG vs Spirit
INSERT INTO Statistics (player_id, match_id, hero_id, kills, deaths, assists, damage, roshan_kills, towers_kills) VALUES
(100000006, 7300000002, 13, 6, 4, 5, 19000, 0, 1),
(100000007, 7300000002, 8, 10, 5, 2, 30000, 0, 2),
(100000008, 7300000002, 20, 9, 3, 4, 27000, 1, 1),
(100000009, 7300000002, 3, 1, 2, 11, 6000, 0, 1),
(100000010, 7300000002, 9, 2, 5, 13, 7000, 0, 1),
(100000001, 7300000002, 16, 5, 3, 9, 20000, 0, 2),
(100000002, 7300000002, 6, 14, 4, 3, 35000, 0, 3),
(100000003, 7300000002, 18, 6, 6, 7, 21000, 0, 1),
(100000004, 7300000002, 17, 4, 1, 16, 12000, 0, 2),
(100000005, 7300000002, 12, 3, 3, 12, 10000, 0, 1);

-- Додамо ще 2 матчі для прикладу (ти можеш продовжити за аналогією)
-- Match 7300000003: Liquid vs BetBoom
INSERT INTO Statistics (player_id, match_id, hero_id, kills, deaths, assists, damage, roshan_kills, towers_kills) VALUES
(100000011, 7300000003, 5, 1, 2, 15, 5500, 0, 1),
(100000012, 7300000003, 15, 11, 4, 2, 31000, 0, 3),
(100000013, 7300000003, 10, 7, 3, 8, 24000, 0, 2),
(100000014, 7300000003, 2, 4, 5, 6, 17000, 0, 1),
(100000015, 7300000003, 19, 2, 3, 10, 8000, 0, 1),
(100000016, 7300000003, 13, 5, 6, 4, 18000, 0, 1),
(100000017, 7300000003, 14, 8, 5, 3, 26000, 0, 2),
(100000018, 7300000003, 1, 9, 7, 1, 29000, 0, 2),
(100000019, 7300000003, 11, 3, 4, 9, 11000, 0, 1),
(100000020, 7300000003, 7, 2, 2, 14, 9500, 1, 2);

-- Match 7300000004: BetBoom vs Liquid
INSERT INTO Statistics (player_id, match_id, hero_id, kills, deaths, assists, damage, roshan_kills, towers_kills) VALUES
(100000016, 7300000004, 16, 3, 5, 7, 15000, 0, 1),
(100000017, 7300000004, 20, 6, 4, 5, 23000, 0, 1),
(100000018, 7300000004, 8, 10, 6, 2, 33000, 0, 3),
(100000019, 7300000004, 9, 1, 3, 12, 6500, 0, 1),
(100000020, 7300000004, 3, 2, 4, 11, 7500, 0, 1),
(100000011, 7300000004, 12, 4, 3, 13, 13000, 0, 2),
(100000012, 7300000004, 6, 13, 5, 1, 36000, 0, 3),
(100000013, 7300000004, 18, 5, 7, 6, 20000, 0, 1),
(100000014, 7300000004, 2, 6, 6, 5, 21000, 0, 2),
(100000015, 7300000004, 17, 3, 2, 15, 11000, 0, 2);

-- Додамо ще 16 матчів статистики (скорочено — ти можеш продовжити за шаблоном)
-- Для економії місця — додамо по 1 рядку на матч
INSERT INTO Statistics (player_id, match_id, hero_id, kills, deaths, assists, damage, roshan_kills, towers_kills) VALUES
(100000021, 7300000005, 1, 11, 4, 3, 34000, 0, 2),
(100000026, 7300000006, 14, 7, 6, 4, 25000, 0, 1),
(100000031, 7300000007, 5, 0, 5, 16, 4000, 0, 1),
(100000036, 7300000008, 19, 3, 4, 10, 9000, 0, 1),
(100000002, 7300000009, 8, 15, 3, 2, 40000, 1, 3),
(100000012, 7300000010, 15, 10, 5, 1, 32000, 0, 2),
(100000007, 7300000011, 6, 12, 4, 2, 37000, 0, 3),
(100000018, 7300000012, 1, 8, 6, 3, 27000, 0, 2),
(100000021, 7300000013, 8, 13, 4, 3, 38000, 0, 3),
(100000034, 7300000014, 14, 9, 5, 4, 30000, 0, 2),
(100000028, 7300000015, 15, 11, 3, 2, 35000, 0, 3),
(100000038, 7300000016, 1, 10, 5, 2, 33000, 0, 2),
(100000001, 7300000017, 2, 6, 3, 9, 22000, 0, 2),
(100000023, 7300000018, 16, 4, 4, 7, 18000, 0, 1),
(100000014, 7300000019, 2, 5, 5, 8, 20000, 0, 2),
(100000035, 7300000020, 13, 7, 6, 5, 24000, 0, 2);

-- Призові місця
INSERT INTO Prizes (tournament_id, team_id, place, amount) VALUES
(15476, 9565, 1, 5000000.00),      -- Team Spirit — 1 місце
(15476, 111494, 2, 2000000.00),    -- Gaimin Gladiators — 2 місце
(15476, 894029, 3, 1200000.00),    -- Team Liquid — 3 місце
(15476, 116387, 4, 800000.00);     -- BetBoom Team — 4 місце