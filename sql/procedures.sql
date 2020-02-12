DROP FUNCTION IF EXISTS angle_to_decimal;
DROP PROCEDURE IF EXISTS decimal_to_angle;
DROP PROCEDURE IF EXISTS period_from_orbit;
DROP PROCEDURE IF EXISTS check_discoveries;
DROP TRIGGER IF EXISTS one_discovery_update;
DROP TRIGGER IF EXISTS one_discovery_insert;

delimiter //

CREATE FUNCTION angle_to_decimal(degrees INT, minutes INT, seconds DECIMAL(10, 8))
    RETURNS DECIMAL(16, 8) DETERMINISTIC
BEGIN
    IF degrees >= 0 THEN
        RETURN degrees + minutes/60 + seconds/3600;
    ELSE
        RETURN degrees - minutes/60 - seconds/3600;
    END IF;
END//

CREATE PROCEDURE decimal_to_angle(angle DECIMAL(16, 8), OUT degrees INT, OUT minutes INT, 
    OUT seconds DECIMAL(10, 8)) DETERMINISTIC
BEGIN
    SET degrees = TRUNCATE(angle, 0);
    SET minutes = TRUNCATE(ABS(angle - degrees) * 60, 0);
    SET seconds = (ABS(angle - degrees) - minutes/60) * 3600;
END//

CREATE PROCEDURE period_from_orbit(name VARCHAR(70)) MODIFIES SQL DATA
BEGIN
    DECLARE is_small_body INT;
    DECLARE orbited_star VARCHAR(70);
    DECLARE orbited_body VARCHAR(70);

    SELECT count(*) INTO is_small_body FROM male_cialo WHERE nazwa = name;
    IF is_small_body > 0 THEN
        SELECT orbitowana_gwiazda, orbitowane_male_cialo
        INTO orbited_star, orbited_body
        FROM male_cialo WHERE nazwa = name;
        
        IF orbited_star = 'Sun' OR orbited_star = 'Slonce' THEN
            UPDATE male_cialo
            SET okres = POW(polos_wielka, 1.5)
            WHERE nazwa = name;
        ELSEIF orbited_body = 'Earth' OR orbited_body = 'Ziemia' THEN
            UPDATE male_cialo
            SET okres = POW(polos_wielka, 1.5) * 577.014768783
            WHERE nazwa = name;
        END IF;
    ELSE
        SELECT orbitowana_gwiazda, orbitowane_male_cialo
        INTO orbited_star, orbited_body
        FROM sztuczny_satelita WHERE nazwa = name;

        IF orbited_star = 'Sun' OR orbited_star = 'Slonce' THEN
            UPDATE sztuczny_satelita
            SET okres = 2 * PI() * POW((apocentrum + perycentrum + 12742)/(2 * 17286.786135), 1.5) / 577.014768783
            WHERE nazwa = name;
        ELSEIF orbited_body = 'Earth' OR orbited_body = 'Ziemia' THEN
            UPDATE sztuczny_satelita
            SET okres = 2 * PI() * POW((apocentrum + perycentrum + 12742)/(2 * 17286.786135), 1.5)
            WHERE nazwa = name;
        END IF;
    END IF;
END//

CREATE PROCEDURE check_discoveries(was_discovery BOOL, is_discovery BOOL, object VARCHAR(70))
BEGIN
    DECLARE discoveries_count INT;

    IF is_discovery AND NOT was_discovery THEN
        SELECT COUNT(*) INTO discoveries_count FROM obserwacja
        WHERE obiekt_astronomiczny = object AND czy_odkrycie;

        IF discoveries_count > 0 THEN
            SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'There can be only one discovery per object',
                MYSQL_ERRNO = 1644;
        END IF;
    END IF;
END;

CREATE TRIGGER one_discovery_update BEFORE UPDATE ON obserwacja
FOR EACH ROW CALL check_discoveries(OLD.czy_odkrycie, NEW.czy_odkrycie, NEW.obiekt_astronomiczny)//

CREATE TRIGGER one_discovery_insert BEFORE INSERT ON obserwacja
FOR EACH ROW CALL check_discoveries(FALSE, NEW.czy_odkrycie, NEW.obiekt_astronomiczny)//

delimiter ;
