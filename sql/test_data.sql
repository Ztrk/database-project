INSERT INTO astronom(pelne_imie, data_urodzenia, data_zgonu, kraj, imie_mpc) VALUES
('Abc Def', '1970-08-11', null, 'USA', 'Abc Def');

INSERT INTO obserwatorium(kod_iau, szerokosc_geograficzna, dlugosc_geograficzna,
    kraj, pelna_nazwa, nazwa_mpc) VALUES
('G84', 32.4425, -110.7892, 'USA', 'Mount Lemmon Sky Center', 'Mount Lemmon Sky Center');

INSERT INTO konstelacja(skrot_iau, nazwa, najjasniejsza_gwiazda) VALUES
('And', 'Andromeda', 'Alpheratz'),
('Tau', 'Taurus', 'Aldebaran'),
('Sgr', 'Sagittarius', 'Epsilon Sagittarii'),
('Sct', 'Scutum', 'Alpha Scuti');

INSERT INTO obiekt_astronomiczny(nazwa) VALUES
('Earth'),
('Moon'),
('1P/Halley'),
('Sun'),
('International Space Station'),
('Aldebaran'),
('Milky Way'),
('Andromeda Galaxy'),
('192686 Aljuroma'),
("Stephan's Quintet"),
('Local Group'),
('Perseids'),
('Orionids');

INSERT INTO grupa_galaktyk(nazwa, rektasencja, deklinacja, dystans, predkosc_radialna) VALUES
("Stephan's Quintet", 22.5993, 33.96, 300, 6600),
('Local Group', null, null, null, null);

INSERT INTO galaktyka(nazwa, typ, rektasencja, deklinacja, wielkosc_obserwowana, 
    wielkosc_absolutna, dystans, srednica, grupa_galaktyk, konstelacja) VALUES
('Milky Way', 'Sb', null, null, null, -20.9, 0, 175, 'Local Group', null),
('Andromeda Galaxy', 'SA(s)b', 0.712306, 41.269167, 3.44, -21.5, 2.54, 220, 'Local Group', 'And');

INSERT INTO gwiazda(nazwa, typ_widmowy, rektasencja, deklinacja, wielkosc_obserwowana, 
    wielkosc_absolutna, dystans, paralaksa, masa, promien, galaktyka, konstelacja) VALUES
('Sun', 'G2V', null, null, -26.74, 4.83, 0, null, 1, 1, 'Milky Way', null),
('Aldebaran', 'K5+ III', 4.598678, 16.509302, 0.85, -0.641, 65.3, 49.97, 1.16, 44.13, 'Milky Way', 'Tau');

INSERT INTO male_cialo(nazwa, typ, okres, ekscentrycznosc, polos_wielka, inklinacja,
    srednica, masa, orbitowana_gwiazda, orbitowane_male_cialo, temperatura) VALUES
('Earth', 'Planeta', 1, 0.0167, 1, 0, 12742, 1, 'Sun', null, 287.16),
('Moon', 'Satelita', 0.0748, 0.0549, 0.00257, 5.145, 3474.8, 0.0123, null, 'Earth', 220),
('192686 Aljuroma', 'Asteroida', 4.36, 0.3804, 2.6699, 11.2820, 3.5, null, 'Sun', null, null),
('1P/Halley', 'Kometa', 75.32, 0.96714, 17.834, 162.26, 11, null, 'Sun', null, null);

INSERT INTO sztuczny_satelita(nazwa, okres, apocentrum, perycentrum, inklinacja, data_startu, 
    data_zniszczenia, kraj, rodzaj, orbitowana_gwiazda, orbitowane_male_cialo) VALUES
('International Space Station', 1.5447, 410, 408, 51.64, '1998-10-20', null, 'International', 'Stacja kosmiczna', null, 'Earth');

INSERT INTO roj_meteorow(nazwa, data_poczatku, data_konca, data_maksimum, 
    rektasencja, deklinacja, predkosc, zhr, aktywnosc) VALUES
('Perseids', '2000-07-17', '2000-08-24', '2000-08-12', 3.0667, 58, 58, 100, 'high'),
('Orionids', '2000-10-02', '2000-11-07', '2000-10-21', 6.4, 15, 66.9, 20, 'high');

INSERT INTO katalog(nazwa, skrot, rok_wydania) VALUES
('Henry Draper Catalogue', 'HD', '1918');

INSERT INTO obserwacja(data, obiekt_astronomiczny, obserwatorium, astronom, czy_odkrycie) VALUES
('2019-02-13', '192686 Aljuroma', 'G84', 'Abc Def', 0);
