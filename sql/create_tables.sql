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

ALTER TABLE astronom ADD CONSTRAINT astronomer_date_check
CHECK (data_zgonu >= data_urodzenia);

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
FOREIGN KEY (nazwa) REFERENCES obiekt_astronomiczny (nazwa) ON UPDATE CASCADE;

ALTER TABLE grupa_galaktyk ADD CONSTRAINT galaxy_group_right_ascension_check
CHECK (rektasencja >= 0 AND rektasencja <= 24);

ALTER TABLE grupa_galaktyk ADD CONSTRAINT galaxy_group_declination_check
CHECK (deklinacja >= -90 AND deklinacja <= 90);

ALTER TABLE grupa_galaktyk ADD CONSTRAINT galaxy_group_distance_check
CHECK (dystans >= 0);

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
FOREIGN KEY (nazwa) REFERENCES obiekt_astronomiczny (nazwa) ON UPDATE CASCADE;

ALTER TABLE galaktyka ADD CONSTRAINT galaktyka_grupa_galaktyk_fk
FOREIGN KEY (grupa_galaktyk) REFERENCES grupa_galaktyk (nazwa) ON UPDATE CASCADE;

ALTER TABLE galaktyka ADD CONSTRAINT orbitowana_galaktyka_fk
FOREIGN KEY (orbitowana_galaktyka) REFERENCES galaktyka (nazwa) ON UPDATE CASCADE;

ALTER TABLE galaktyka ADD CONSTRAINT galaktyka_konstelacja_fk
FOREIGN KEY (konstelacja) REFERENCES konstelacja (skrot_iau);

ALTER TABLE galaktyka ADD CONSTRAINT galaxy_right_ascension_check
CHECK (rektasencja >= 0 AND rektasencja <= 24);

ALTER TABLE galaktyka ADD CONSTRAINT galaxy_declination_check
CHECK (deklinacja >= -90 AND deklinacja <= 90);

ALTER TABLE galaktyka ADD CONSTRAINT galaxy_distance_check
CHECK (dystans >= 0);

ALTER TABLE galaktyka ADD CONSTRAINT galaxy_diameter_check
CHECK (srednica >= 0);

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
FOREIGN KEY (nazwa) REFERENCES obiekt_astronomiczny (nazwa) ON UPDATE CASCADE;

ALTER TABLE gwiazda ADD CONSTRAINT gwiazda_galaktyka_fk
FOREIGN KEY (galaktyka) REFERENCES galaktyka (nazwa) ON UPDATE CASCADE;

ALTER TABLE gwiazda ADD CONSTRAINT gwiazda_konstelacja_fk
FOREIGN KEY (konstelacja) REFERENCES konstelacja (skrot_iau);

ALTER TABLE gwiazda ADD CONSTRAINT star_right_ascension_check
CHECK (rektasencja >= 0 AND rektasencja <= 24);

ALTER TABLE gwiazda ADD CONSTRAINT star_declination_check
CHECK (deklinacja >= -90 AND deklinacja <= 90);

ALTER TABLE gwiazda ADD CONSTRAINT star_distance_check
CHECK (dystans >= 0);

ALTER TABLE gwiazda ADD CONSTRAINT star_parallax_check
CHECK (paralaksa >= 0);

ALTER TABLE gwiazda ADD CONSTRAINT star_mass_check
CHECK (masa >= 0);

ALTER TABLE gwiazda ADD CONSTRAINT star_radius_check
CHECK (promien >= 0);

CREATE TABLE male_cialo (
    nazwa                        VARCHAR(70) NOT NULL,
    typ                          VARCHAR(30),
    okres                        DECIMAL(10, 6), 
    ekscentrycznosc              DECIMAL(10, 6) NOT NULL, 
    polos_wielka                 DECIMAL(10, 6) NOT NULL, 
    inklinacja                   DECIMAL(10, 6) NOT NULL, 
    srednica                     DECIMAL(10, 4) NOT NULL, 
    masa                         DECIMAL(12, 6),
    orbitowana_gwiazda           VARCHAR(70),
    orbitowane_male_cialo        VARCHAR(70),
    temperatura                  DECIMAL(8, 2)
);

ALTER TABLE male_cialo ADD CONSTRAINT male_cialo_pk PRIMARY KEY (nazwa);

ALTER TABLE male_cialo ADD CONSTRAINT male_cialo_obiekt_astronomiczny_fk
FOREIGN KEY (nazwa) REFERENCES obiekt_astronomiczny (nazwa) ON UPDATE CASCADE;

ALTER TABLE male_cialo ADD CONSTRAINT orbitowana_gwiazda_fk
FOREIGN KEY (orbitowana_gwiazda) REFERENCES gwiazda (nazwa) ON UPDATE CASCADE;

ALTER TABLE male_cialo ADD CONSTRAINT orbitowane_cialo_fk
FOREIGN KEY (orbitowane_male_cialo) REFERENCES male_cialo (nazwa) ON UPDATE CASCADE;

ALTER TABLE male_cialo ADD CONSTRAINT small_body_period_check
CHECK (okres >= 0);

ALTER TABLE male_cialo ADD CONSTRAINT small_body_eccentricity_check
CHECK (ekscentrycznosc >= 0);

ALTER TABLE male_cialo ADD CONSTRAINT small_body_semi_major_axis_check
CHECK (polos_wielka >= 0);

ALTER TABLE male_cialo ADD CONSTRAINT small_body_inclination_check
CHECK (inklinacja >= 0 AND inklinacja <= 180);

ALTER TABLE male_cialo ADD CONSTRAINT small_body_mass_check
CHECK (masa >= 0);

ALTER TABLE male_cialo ADD CONSTRAINT small_body_diameter_check
CHECK (srednica >= 0);

CREATE TABLE sztuczny_satelita (
    nazwa                   VARCHAR(70) NOT NULL,
    okres                   DECIMAL(10, 6), 
    apocentrum              DECIMAL(10, 6) NOT NULL, 
    perycentrum             DECIMAL(10, 6) NOT NULL, 
    inklinacja              DECIMAL(10, 6) NOT NULL,
    data_startu             DATE NOT NULL,
    data_zniszczenia        DATE,
    kraj                    VARCHAR(50) NOT NULL,
    rodzaj                  VARCHAR(20) NOT NULL,
    orbitowana_gwiazda      VARCHAR(70),
    orbitowane_male_cialo   VARCHAR(70)
);

ALTER TABLE sztuczny_satelita ADD CONSTRAINT sztuczny_satelita_pk PRIMARY KEY (nazwa);

ALTER TABLE sztuczny_satelita ADD CONSTRAINT sztuczny_satelita_obiekt_astronomiczny_fk
FOREIGN KEY (nazwa) REFERENCES obiekt_astronomiczny (nazwa) ON UPDATE CASCADE;

ALTER TABLE sztuczny_satelita ADD CONSTRAINT sztuczny_satelita_gwiazda_fk
FOREIGN KEY (orbitowana_gwiazda) REFERENCES gwiazda (nazwa) ON UPDATE CASCADE;

ALTER TABLE sztuczny_satelita ADD CONSTRAINT sztuczny_satelita_male_ciala_fk
FOREIGN KEY (orbitowane_male_cialo) REFERENCES male_cialo (nazwa) ON UPDATE CASCADE;

ALTER TABLE sztuczny_satelita ADD CONSTRAINT satellite_period_chck
CHECK (okres >= 0);

ALTER TABLE sztuczny_satelita ADD CONSTRAINT satellite_inclination_check
CHECK (inklinacja >= 0 AND inklinacja <= 180);

ALTER TABLE sztuczny_satelita ADD CONSTRAINT satellite_date_check
CHECK (data_zniszczenia >= data_startu);

CREATE TABLE roj_meteorow (
    nazwa           VARCHAR(70) NOT NULL,
    data_poczatku   DATE NOT NULL,
    data_konca      DATE NOT NULL,
    data_maksimum   DATE NOT NULL,
    rektasencja     DECIMAL(10, 6) NOT NULL, 
    deklinacja      DECIMAL(10, 6) NOT NULL,
    predkosc        DECIMAL(5, 2) NOT NULL,
    zhr             DECIMAL(6, 3) NOT NULL,
    aktywnosc       VARCHAR(20) NOT NULL
);

ALTER TABLE roj_meteorow ADD CONSTRAINT roj_meteorow_pk PRIMARY KEY (nazwa);

ALTER TABLE roj_meteorow ADD CONSTRAINT roj_meteorow_obiekt_astronomiczny_fk
FOREIGN KEY (nazwa) REFERENCES obiekt_astronomiczny (nazwa) ON UPDATE CASCADE;

ALTER TABLE roj_meteorow ADD CONSTRAINT meteor_shower_right_ascension_check
CHECK (rektasencja >= 0 AND rektasencja <= 24);

ALTER TABLE roj_meteorow ADD CONSTRAINT meteor_shower_declination_check
CHECK (deklinacja >= -90 AND deklinacja <= 90);

ALTER TABLE roj_meteorow ADD CONSTRAINT meteor_shower_velocity_check
CHECK (predkosc >= 0);

ALTER TABLE roj_meteorow ADD CONSTRAINT meteor_shower_zhr_check
CHECK (zhr >= 0);

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
FOREIGN KEY (katalog_nazwa) REFERENCES katalog (nazwa) ON UPDATE CASCADE;

ALTER TABLE obiekt_w_katalogu ADD CONSTRAINT obiekt_w_katalogu_obiekt_astronomiczny_fk
FOREIGN KEY (obiekt_nazwa) REFERENCES obiekt_astronomiczny (nazwa) ON UPDATE CASCADE;

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
FOREIGN KEY (obiekt_astronomiczny) REFERENCES obiekt_astronomiczny (nazwa) ON UPDATE CASCADE;

ALTER TABLE obserwacja ADD CONSTRAINT obserwacja_obserwatorium_fk
FOREIGN KEY (obserwatorium) REFERENCES obserwatorium (kod_iau);

ALTER TABLE obserwacja ADD CONSTRAINT obserwacja_astronom_fk
FOREIGN KEY (astronom) REFERENCES astronom (pelne_imie) ON UPDATE CASCADE;
