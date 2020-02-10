DROP TABLE IF EXISTS obserwacja;
DROP TABLE IF EXISTS obiekt_w_katalogu;
DROP TABLE IF EXISTS katalog;
DROP TABLE IF EXISTS sztuczny_satelita;
DROP TABLE IF EXISTS male_cialo;
DROP TABLE IF EXISTS gwiazda;
DROP TABLE IF EXISTS galaktyka;
DROP TABLE IF EXISTS grupa_galaktyk;
DROP TABLE IF EXISTS roj_meteorow;
DROP TABLE IF EXISTS obiekt_astronomiczny;
DROP TABLE IF EXISTS konstelacja;
DROP TABLE IF EXISTS astronom;
DROP TABLE IF EXISTS obserwatorium;

CREATE TABLE astronom (
    pelne_imie       VARCHAR(50) NOT NULL,
    data_urodzenia   DATE NOT NULL,
    data_zgonu       DATE,
    kraj             VARCHAR(50) NOT NULL,
    imie_mpc         VARCHAR(20) NOT NULL
);

ALTER TABLE astronom ADD CONSTRAINT astronom_pk PRIMARY KEY (pelne_imie);

CREATE TABLE obserwatorium (
    kod_iau                  VARCHAR(6) NOT NULL,
    szerokosc_geograficzna   DECIMAL(10, 6),
    dlugosc_geograficzna     DECIMAL(10, 6),
    kraj                     VARCHAR(50) NOT NULL,
    pelna_nazwa              VARCHAR(70) NOT NULL,
    nazwa_mpc                VARCHAR(30) NOT NULL
);

ALTER TABLE obserwatorium ADD CONSTRAINT obserwatorium_pk PRIMARY KEY (kod_iau);

ALTER TABLE obserwatorium ADD CONSTRAINT latitude_check
CHECK (szerokosc_geograficzna >= -90 AND szerokosc_geograficzna <= 90);

ALTER TABLE obserwatorium ADD CONSTRAINT longitude_check
CHECK (dlugosc_geograficzna >= -180 AND dlugosc_geograficzna <= 180);

ALTER TABLE obserwatorium ADD CONSTRAINT coordinates_present
CHECK ((szerokosc_geograficzna IS NULL AND dlugosc_geograficzna IS NULL)
    OR (szerokosc_geograficzna IS NOT NULL AND dlugosc_geograficzna IS NOT NULL));

CREATE TABLE konstelacja (
    skrot_iau               VARCHAR(8) NOT NULL,
    nazwa                   VARCHAR(50) NOT NULL,
    najjasniejsza_gwiazda   VARCHAR(50) NOT NULL
);

ALTER TABLE konstelacja ADD CONSTRAINT konstelacja_pk PRIMARY KEY (skrot_iau);

CREATE TABLE obiekt_astronomiczny (
    nazwa VARCHAR(70) NOT NULL
);

ALTER TABLE obiekt_astronomiczny ADD CONSTRAINT obiekt_astronomiczny_pk PRIMARY KEY (nazwa);

CREATE TABLE grupa_galaktyk (
    nazwa               VARCHAR(70) NOT NULL,
    rektasencja         DECIMAL(10, 6),
    deklinacja          DECIMAL(10, 6),
    dystans             DECIMAL(10, 4),
    predkosc_radialna   DECIMAL(10, 4)
);

ALTER TABLE grupa_galaktyk ADD CONSTRAINT grupa_galaktyk_pk PRIMARY KEY (nazwa);

ALTER TABLE grupa_galaktyk ADD CONSTRAINT grupa_galaktyk_obiekt_astronomiczny_fk
FOREIGN KEY (nazwa) REFERENCES obiekt_astronomiczny (nazwa);

ALTER TABLE grupa_galaktyk ADD CONSTRAINT galaxy_group_right_ascension_check
CHECK (rektasencja >= 0 AND rektasencja <= 24);

ALTER TABLE grupa_galaktyk ADD CONSTRAINT galaxy_group_declination_check
CHECK (deklinacja >= -90 AND deklinacja <= 90);

CREATE TABLE galaktyka (
    nazwa                  VARCHAR(70) NOT NULL,
    typ                    VARCHAR(20) NOT NULL,
    rektasencja            DECIMAL(10, 6),
    deklinacja             DECIMAL(10, 6),
    wielkosc_obserwowana   DECIMAL(6, 4),
    wielkosc_absolutna     DECIMAL(6, 4) NOT NULL,
    dystans                DECIMAL(10, 4),
    srednica               DECIMAL(10, 4) NOT NULL,
    grupa_galaktyk         VARCHAR(70),
    orbitowana_galaktyka   VARCHAR(70),
    konstelacja            VARCHAR(8)
);

ALTER TABLE galaktyka ADD CONSTRAINT galaktyka_pk PRIMARY KEY (nazwa);

ALTER TABLE galaktyka ADD CONSTRAINT galaktyka_obiekt_astronomiczny_fk
FOREIGN KEY (nazwa) REFERENCES obiekt_astronomiczny (nazwa);

ALTER TABLE galaktyka ADD CONSTRAINT galaktyka_grupa_galaktyk_fk
FOREIGN KEY (grupa_galaktyk) REFERENCES grupa_galaktyk (nazwa);

ALTER TABLE galaktyka ADD CONSTRAINT orbitowana_galaktyka_fk
FOREIGN KEY (orbitowana_galaktyka) REFERENCES galaktyka (nazwa);

ALTER TABLE galaktyka ADD CONSTRAINT galaktyka_konstelacja_fk
FOREIGN KEY (konstelacja) REFERENCES konstelacja (skrot_iau);

ALTER TABLE galaktyka ADD CONSTRAINT galaxy_right_ascension_check
CHECK (rektasencja >= 0 AND rektasencja <= 24);

ALTER TABLE galaktyka ADD CONSTRAINT galaxy_declination_check
CHECK (deklinacja >= -90 AND deklinacja <= 90);

CREATE TABLE gwiazda (
    nazwa                  VARCHAR(70) NOT NULL,
    typ_widmowy            VARCHAR(20) NOT NULL,
    rektasencja            DECIMAL(10, 6),
    deklinacja             DECIMAL(10, 6),
    wielkosc_obserwowana   DECIMAL(6, 4) NOT NULL,
    wielkosc_absolutna     DECIMAL(6, 4) NOT NULL,
    dystans                DECIMAL(10, 4) NOT NULL,
    paralaksa              DECIMAL(10, 4),
    masa                   DECIMAL(10, 4) NOT NULL,
    promien                DECIMAL(10, 4) NOT NULL,
    galaktyka              VARCHAR(70) NOT NULL,
    konstelacja            VARCHAR(8)
);

ALTER TABLE gwiazda ADD CONSTRAINT gwiazda_pk PRIMARY KEY (nazwa);

ALTER TABLE gwiazda ADD CONSTRAINT gwiazda_obiekt_astronomiczny_fk
FOREIGN KEY (nazwa) REFERENCES obiekt_astronomiczny (nazwa);

ALTER TABLE gwiazda ADD CONSTRAINT gwiazda_galaktyka_fk
FOREIGN KEY (galaktyka) REFERENCES galaktyka (nazwa);

ALTER TABLE gwiazda ADD CONSTRAINT gwiazda_konstelacja_fk
FOREIGN KEY (konstelacja) REFERENCES konstelacja (skrot_iau);

ALTER TABLE gwiazda ADD CONSTRAINT star_right_ascension_check
CHECK (rektasencja >= 0 AND rektasencja <= 24);

ALTER TABLE gwiazda ADD CONSTRAINT star_declination_check
CHECK (deklinacja >= -90 AND deklinacja <= 90);

CREATE TABLE male_cialo (
    nazwa                        VARCHAR(70) NOT NULL,
    typ                          VARCHAR(30),
    okres                        DECIMAL(10, 4),
    ekscentrycznosc              DECIMAL(8, 6) NOT NULL,
    polos_wielka                 DECIMAL(10, 4) NOT NULL,
    inklinacja                   DECIMAL(7, 4) NOT NULL,
    dlugosc_wezla_wstepujacego   DECIMAL(7, 4) NOT NULL,
    argument_perycentrum         DECIMAL(7, 4) NOT NULL,
    anomalia_srednia             DECIMAL(7, 4) NOT NULL,
    epoch                        DECIMAL(10, 4) NOT NULL,
    srednica                     DECIMAL(10, 4) NOT NULL,
    masa                         DECIMAL(10, 4),
    orbitowana_gwiazda           VARCHAR(70),
    orbitowane_male_cialo        VARCHAR(70),
    srednia_temperatura          DECIMAL(8, 2)
);

ALTER TABLE male_cialo ADD CONSTRAINT male_cialo_pk PRIMARY KEY (nazwa);

ALTER TABLE male_cialo ADD CONSTRAINT male_cialo_obiekt_astronomiczny_fk
FOREIGN KEY (nazwa) REFERENCES obiekt_astronomiczny (nazwa);

ALTER TABLE male_cialo ADD CONSTRAINT orbitowana_gwiazda_fk
FOREIGN KEY (orbitowana_gwiazda) REFERENCES gwiazda (nazwa);

ALTER TABLE male_cialo ADD CONSTRAINT orbitowane_cialo_fk
FOREIGN KEY (orbitowane_male_cialo) REFERENCES male_cialo (nazwa);

ALTER TABLE male_cialo ADD CONSTRAINT male_cialo_orbitowane_cialo
CHECK ((orbitowane_male_cialo IS NOT NULL AND orbitowana_gwiazda IS NULL)
      OR (orbitowane_male_cialo IS NULL AND orbitowana_gwiazda IS NOT NULL)
      OR (orbitowane_male_cialo IS NULL AND orbitowana_gwiazda IS NULL));

CREATE TABLE sztuczny_satelita (
    nazwa                   VARCHAR(70) NOT NULL,
    okres_orbitalny         DECIMAL(10, 4),
    apocentrum              DECIMAL(10, 4) NOT NULL,
    perycentrum             DECIMAL(10, 4) NOT NULL,
    inklinacja              DECIMAL(7, 4) NOT NULL,
    data_startu             DATE NOT NULL,
    data_zniszczenia        DATE,
    kraj                    VARCHAR(50) NOT NULL,
    rodzaj                  VARCHAR(20) NOT NULL,
    orbitowana_gwiazda      VARCHAR(70),
    orbitowane_male_cialo   VARCHAR(70)
);

ALTER TABLE sztuczny_satelita ADD CONSTRAINT sztuczny_satelita_pk PRIMARY KEY (nazwa);

ALTER TABLE sztuczny_satelita ADD CONSTRAINT sztuczny_satelita_obiekt_astronomiczny_fk
FOREIGN KEY (nazwa) REFERENCES obiekt_astronomiczny (nazwa);

ALTER TABLE sztuczny_satelita ADD CONSTRAINT sztuczny_satelita_gwiazda_fk
FOREIGN KEY (orbitowana_gwiazda) REFERENCES gwiazda (nazwa);

ALTER TABLE sztuczny_satelita ADD CONSTRAINT sztuczny_satelita_male_ciala_fk
FOREIGN KEY (orbitowane_male_cialo) REFERENCES male_cialo (nazwa);

ALTER TABLE sztuczny_satelita ADD CONSTRAINT satelita_orbitowane_cialo
CHECK ((orbitowana_gwiazda IS NOT NULL AND orbitowane_male_cialo IS NULL)
      OR (orbitowana_gwiazda IS NULL AND orbitowane_male_cialo IS NOT NULL)
      OR (orbitowana_gwiazda IS NULL AND orbitowane_male_cialo IS NULL));

CREATE TABLE roj_meteorow (
    nazwa           VARCHAR(70) NOT NULL,
    data_poczatku   DATE NOT NULL,
    data_końca      DATE NOT NULL,
    data_maksimum   DATE NOT NULL,
    rektasencja     DECIMAL(10, 6) NOT NULL,
    deklinacja      DECIMAL(10, 6) NOT NULL,
    predkosc        DECIMAL(5, 2) NOT NULL,
    zhr             DECIMAL(6, 3) NOT NULL,
    aktywność       VARCHAR(20) NOT NULL
);

ALTER TABLE roj_meteorow ADD CONSTRAINT roj_meteorow_pk PRIMARY KEY (nazwa);

ALTER TABLE roj_meteorow ADD CONSTRAINT roj_meteorow_obiekt_astronomiczny_fk
FOREIGN KEY (nazwa) REFERENCES obiekt_astronomiczny (nazwa);

ALTER TABLE roj_meteorow ADD CONSTRAINT meteor_shower_right_ascension_check
CHECK (rektasencja >= 0 AND rektasencja <= 24);

ALTER TABLE roj_meteorow ADD CONSTRAINT meteor_shower_declination_check
CHECK (deklinacja >= -90 AND deklinacja <= 90);

CREATE TABLE katalog (
    nazwa         VARCHAR(50) NOT NULL,
    skrot         VARCHAR(10) NOT NULL,
    rok_wydania   SMALLINT NOT NULL
);

ALTER TABLE katalog ADD CONSTRAINT katalog_pk PRIMARY KEY (nazwa);

CREATE TABLE obiekt_w_katalogu (
    obiekt_nazwa    VARCHAR(70) NOT NULL,
    katalog_nazwa   VARCHAR(50) NOT NULL
);

ALTER TABLE obiekt_w_katalogu ADD CONSTRAINT obiekt_w_katalogu_pk
PRIMARY KEY (obiekt_nazwa, katalog_nazwa);

ALTER TABLE obiekt_w_katalogu ADD CONSTRAINT obiekt_w_katalogu_katalog_fk
FOREIGN KEY (katalog_nazwa) REFERENCES katalog (nazwa);

ALTER TABLE obiekt_w_katalogu ADD CONSTRAINT obiekt_w_katalogu_obiekt_astronomiczny_fk
FOREIGN KEY (obiekt_nazwa) REFERENCES obiekt_astronomiczny (nazwa);

CREATE TABLE obserwacja (
    data                   DATETIME NOT NULL,
    obiekt_astronomiczny   VARCHAR(70) NOT NULL,
    obserwatorium          VARCHAR(6) NOT NULL,
    astronom               VARCHAR(50) NOT NULL,
    czy_odkrycie           BOOL NOT NULL
);

ALTER TABLE obserwacja ADD CONSTRAINT obserwacja_pk
PRIMARY KEY (data, obiekt_astronomiczny, obserwatorium, astronom);

ALTER TABLE obserwacja ADD CONSTRAINT obserwacja_obiekt_astronomiczny_fk
FOREIGN KEY (obiekt_astronomiczny) REFERENCES obiekt_astronomiczny (nazwa);

ALTER TABLE obserwacja ADD CONSTRAINT obserwacja_obserwatorium_fk
FOREIGN KEY (obserwatorium) REFERENCES obserwatorium (kod_iau);

ALTER TABLE obserwacja ADD CONSTRAINT obserwacja_astronom_fk
FOREIGN KEY (astronom) REFERENCES astronom (pelne_imie);

-- Functions and procedures
DROP FUNCTION IF EXISTS JDToDate;
DROP FUNCTION IF EXISTS DateToJD;
DROP PROCEDURE IF EXISTS AllJDToDate;
DROP PROCEDURE IF EXISTS AllDateToJD;
DELIMITER $$
CREATE FUNCTION JDToDate(pJD NUMERIC)
    RETURNS DATE
    -- RETURNS VARCHAR(10)
BEGIN
    DECLARE X NUMERIC; DECLARE Y NUMERIC; DECLARE A NUMERIC; DECLARE B NUMERIC;
    DECLARE C NUMERIC; DECLARE E NUMERIC; DECLARE F NUMERIC; DECLARE R NUMERIC;
    DECLARE M NUMERIC; DECLARE D NUMERIC;
    DECLARE vData VARCHAR(10); DECLARE charR VARCHAR(4);
    DECLARE charM VARCHAR(2); DECLARE charD VARCHAR(2);
    SET X = FLOOR(pJD + 0.5);
    SET Y = FLOOR((X + 32044.5) / 36524.25);
    SET A = X + Y - FLOOR(Y / 4) - 38 + 1524;
    SET B = FLOOR ((A - 122.1) / 365.25);
    SET C = A - FLOOR (365.25 * B);
    SET E = FLOOR (C / 30.61);
    SET F = FLOOR (E / 14);
    SET R = B - 4716 + F;
    SET M = E - 1 - 12 * F;
    SET D = C + pJD + 0.5 - X - FLOOR (153 * E / 5) - 1;
    SET charR = CONVERT(R, CHAR);
    WHILE CHAR_LENGTH(charR) != 4 DO
        SET charR = CONCAT('0', charR);
    END WHILE;
    SET charM = CONVERT(M, CHAR);
    WHILE CHAR_LENGTH(charM) != 2 DO
        SET charM = CONCAT('0', charM);
    END WHILE;
    SET charD = CONVERT(D, CHAR);
    WHILE CHAR_LENGTH(charD) != 2 DO
        SET charD = CONCAT('0', charD);
    END WHILE;
    SET vData = CONCAT(charR, '-', charM, '-', charD);
    -- RETURN vData;
    RETURN (CONVERT(vData, DATE));
END$$

CREATE FUNCTION DateToJD(pDate DATE)
    RETURNS NUMERIC
BEGIN
    DECLARE A NUMERIC;  DECLARE B NUMERIC; DECLARE E NUMERIC;
    DECLARE JD NUMERIC;
    DECLARE R INTEGER; DECLARE M INTEGER; DECLARE D INTEGER;
    SET R = YEAR(pDate);
    SET M = MONTH(pDate);
    SET D = DAY(pDate);
    SET A = 4716 + R + FLOOR((M + 9) / 12);
    SET B = 1729279.5 + 367 * R + FLOOR(275 * M / 9) - FLOOR(7 * A / 4) + D;
    SET E = FLOOR(3 * (FLOOR((A + 83) / 100) + 1) / 4);
    SET JD = B + 38 - E;
    RETURN JD;
END$$

CREATE PROCEDURE AllDateToJD()
BEGIN
    CREATE TEMPORARY TABLE tempDataInfo AS (SELECT pelne_imie,data_urodzenia,data_zgonu FROM astronom);
    ALTER TABLE astronom
        MODIFY COLUMN data_zgonu NUMERIC,
        MODIFY COLUMN data_urodzenia NUMERIC;
    UPDATE astronom t1 INNER JOIN tempDataInfo t2 ON t1.pelne_imie = t2.pelne_imie SET t1.data_urodzenia = DateToJD(t2.data_urodzenia);
    UPDATE astronom t1 INNER JOIN tempDataInfo t2 ON t1.pelne_imie = t2.pelne_imie SET t1.data_zgonu = DateToJD(t2.data_zgonu);
    DROP TEMPORARY TABLE tempDataInfo;

    CREATE TEMPORARY TABLE tempDataInfo AS (SELECT nazwa,data_startu,data_zniszczenia FROM sztuczny_satelita);
    ALTER TABLE sztuczny_satelita
        MODIFY COLUMN data_startu NUMERIC,
        MODIFY COLUMN data_zniszczenia NUMERIC;
    UPDATE sztuczny_satelita t1 INNER JOIN tempDataInfo t2 ON t1.nazwa = t2.nazwa SET t1.data_startu = DateToJD(t2.data_startu);
    UPDATE sztuczny_satelita t1 INNER JOIN tempDataInfo t2 ON t1.nazwa = t2.nazwa SET t1.data_zniszczenia = DateToJD(t2.data_zniszczenia);
    DROP TEMPORARY TABLE tempDataInfo;

    CREATE TEMPORARY TABLE tempDataInfo AS (SELECT nazwa,data_poczatku,data_końca,data_maksimum FROM roj_meteorow);
    ALTER TABLE roj_meteorow
        MODIFY COLUMN data_poczatku NUMERIC,
        MODIFY COLUMN data_końca NUMERIC,
        MODIFY COLUMN data_maksimum NUMERIC;
    UPDATE roj_meteorow t1 INNER JOIN tempDataInfo t2 ON t1.nazwa = t2.nazwa SET t1.data_poczatku = DateToJD(t2.data_poczatku);
    UPDATE roj_meteorow t1 INNER JOIN tempDataInfo t2 ON t1.nazwa = t2.nazwa SET t1.data_końca = DateToJD(t2.data_końca);
    UPDATE roj_meteorow t1 INNER JOIN tempDataInfo t2 ON t1.nazwa = t2.nazwa SET t1.data_maksimum = DateToJD(t2.data_maksimum);
    DROP TEMPORARY TABLE tempDataInfo;
    --
    -- CREATE TEMPORARY TABLE tempDataInfo AS (SELECT data,obiekt_astronomiczny,obserwatorium,astronom FROM obserwacja);
    -- ALTER TABLE obserwacja
    --     MODIFY COLUMN data NUMERIC;
    -- UPDATE obserwacja t1 INNER JOIN tempDataInfo t2 ON (t1.data = t2.data AND t1.obiekt_astronomiczny = t2.obiekt_astronomiczny AND
    -- t1.obserwatorium = t2.obserwatorium AND t1.astronom = t2.astronom) SET t1.data = DateToJD(t2.data);
    -- DROP TEMPORARY TABLE tempDataInfo;
END$$

CREATE PROCEDURE AllJDToDate()
BEGIN
    CREATE TEMPORARY TABLE tempDataInfo AS (SELECT pelne_imie,data_urodzenia,data_zgonu FROM astronom);
    UPDATE astronom SET data_urodzenia = 19990101 WHERE data_urodzenia IS NOT NULL;
    UPDATE astronom SET data_zgonu = 19990101 WHERE data_zgonu IS NOT NULL;
    ALTER TABLE astronom
        MODIFY COLUMN data_zgonu DATE,
        MODIFY COLUMN data_urodzenia DATE;
    UPDATE astronom t1 INNER JOIN tempDataInfo t2 ON t1.pelne_imie = t2.pelne_imie SET t1.data_urodzenia = JDToDate(t2.data_urodzenia);
    UPDATE astronom t1 INNER JOIN tempDataInfo t2 ON t1.pelne_imie = t2.pelne_imie SET t1.data_zgonu = JDToDate(t2.data_zgonu);
    DROP TEMPORARY TABLE tempDataInfo;

    CREATE TEMPORARY TABLE tempDataInfo AS (SELECT nazwa,data_startu,data_zniszczenia FROM sztuczny_satelita);
    UPDATE sztuczny_satelita SET data_startu = 19990101 WHERE data_startu IS NOT NULL;
    UPDATE sztuczny_satelita SET data_zniszczenia = 19990101 WHERE data_zniszczenia IS NOT NULL;
    ALTER TABLE sztuczny_satelita
        MODIFY COLUMN data_startu DATE,
        MODIFY COLUMN data_zniszczenia DATE;
    UPDATE sztuczny_satelita t1 INNER JOIN tempDataInfo t2 ON t1.nazwa = t2.nazwa SET t1.data_startu = JDToDate(t2.data_startu);
    UPDATE sztuczny_satelita t1 INNER JOIN tempDataInfo t2 ON t1.nazwa = t2.nazwa SET t1.data_zniszczenia = JDToDate(t2.data_zniszczenia);
    DROP TEMPORARY TABLE tempDataInfo;

    CREATE TEMPORARY TABLE tempDataInfo AS (SELECT nazwa,data_poczatku,data_końca,data_maksimum FROM roj_meteorow);
    UPDATE roj_meteorow SET data_poczatku = 19990101 WHERE data_poczatku IS NOT NULL;
    UPDATE roj_meteorow SET data_końca = 19990101 WHERE data_końca IS NOT NULL;
    UPDATE roj_meteorow SET data_maksimum = 19990101 WHERE data_maksimum IS NOT NULL;
    ALTER TABLE roj_meteorow
        MODIFY COLUMN data_poczatku DATE,
        MODIFY COLUMN data_końca DATE,
        MODIFY COLUMN data_maksimum DATE;
    UPDATE roj_meteorow t1 INNER JOIN tempDataInfo t2 ON t1.nazwa = t2.nazwa SET t1.data_poczatku = JDToDate(t2.data_poczatku);
    UPDATE roj_meteorow t1 INNER JOIN tempDataInfo t2 ON t1.nazwa = t2.nazwa SET t1.data_końca = JDToDate(t2.data_końca);
    UPDATE roj_meteorow t1 INNER JOIN tempDataInfo t2 ON t1.nazwa = t2.nazwa SET t1.data_maksimum = JDToDate(t2.data_maksimum);
    DROP TEMPORARY TABLE tempDataInfo;
    --
    -- CREATE TEMPORARY TABLE tempDataInfo AS (SELECT data,obiekt_astronomiczny,obserwatorium,astronom FROM obserwacja);
    -- UPDATE obserwacja t1 INNER JOIN tempDataInfo t2 ON (t1.data = t2.data AND t1.obiekt_astronomiczny = t2.obiekt_astronomiczny AND
    -- t1.obserwatorium = t2.obserwatorium AND t1.astronom = t2.astronom) SET t1.data = JDToDate(t2.data);
    -- ALTER TABLE obserwacja
    --     MODIFY COLUMN data DATE;
    -- UPDATE obserwacja t1 INNER JOIN tempDataInfo t2 ON (t1.data = t2.data AND t1.obiekt_astronomiczny = t2.obiekt_astronomiczny AND
    -- t1.obserwatorium = t2.obserwatorium AND t1.astronom = t2.astronom) SET t1.data = JDToDate(t2.data);
    -- DROP TEMPORARY TABLE tempDataInfo;
END$$
DELIMITER ;
