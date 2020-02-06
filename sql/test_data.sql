INSERT INTO astronom(pelne_imie, data_urodzenia, data_zgonu, kraj, imie_mpc) VALUES
('Abc Def', '1970-08-11', null, 'USA', 'Abc Def');

INSERT INTO obserwatorium(kod_iau, szerokosc_geograficzna, dlugosc_geograficzna,
    kraj, pelna_nazwa, nazwa_mpc) VALUES
('G84', 32.4425, -110.7892, 'USA', 'Mount Lemmon Sky Center', 'Mount Lemmon Sky Center');

INSERT INTO konstelacja(skrot_iau, nazwa, najjasniejsza_gwiazda) VALUES
('Sgr', 'Sagittarius', 'Epsilon Sagittarii'),
('Sct', 'Scutum', 'Alpha Scuti');

INSERT INTO obiekt_astronomiczny(nazwa) VALUES
('Venus'),
('Jupiter'),
('Sun'),
('Milky Way'),
('192686 Aljuroma'),
("Stephan's Quintet"),
('Local Group');

INSERT INTO grupa_galaktyk(nazwa, rektasencja, deklinacja, dystans, predkosc_radialna) VALUES
("Stephan's Quintet", 22.5993, 33.96, 300, 6600),
('Local Group', null, null, null, null);

INSERT INTO galaktyka(nazwa, typ, wielkosc_gwiazdowa_absolutna, srednica, grupa_galaktyk) VALUES
('Milky Way', 'Sb', -20.9, 175, 'Local Group');

INSERT INTO katalog(nazwa, skrot, rok_wydania) VALUES
('Henry Draper Catalogue', 'HD', '1918');

INSERT INTO obserwacja(data, obiekt_astronomiczny, obserwatorium, astronom, czy_odkrycie) VALUES
('2019-02-13', '192686 Aljuroma', 'G84', 'Abc Def', 0);
