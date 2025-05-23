-- Zapfstelle (Positionen)
INSERT INTO Zapfstelle (SchienenPos, Pumpe, PumpenNR, Fuellmenge) VALUES
(25,    0, NULL, 1000),   -- Pos1: Vodka (servo)
(525,   0, NULL, 1000),   -- Pos2: Tequila (servo)
(1025,  0, NULL, 1000),   -- Pos3: Bacardi (servo)
(1525,  0, NULL, 1000),   -- Pos4: Rum (servo)
(2025,  0, NULL, 1000),   -- Pos5: Korn (servo)
(2525,  0, NULL, 1000),   -- Pos6: Gin (servo)
(3025,  1, 0,    1000),   -- pump0: Cola (pump)
(3025,  1, 1,    1000),   -- pump1: Orangensaft (pump)
(3025,  1, 2,    1000),   -- pump2: Bananensaft (pump)
(3025,  1, 3,    1000),   -- pump3: Ananassaft (pump)
(3025,  1, 4,    1000),   -- pump4: Tonic Water (pump)
(3025,  1, 5,    1000),   -- pump5: Fanta (pump)
(3025,  1, 6,    1000);   -- pump6: Sprite (pump)

-- Zutaten
INSERT INTO Zutat (Zapfstelle, Name, Alkohol) VALUES
(1,  'Vodka',        1),
(2,  'Tequila',      1),
(3,  'Bacardi',      1),
(4,  'Rum',          1),
(5,  'Korn',         1),
(6,  'Gin',          1),
(7,  'Cola',         0),
(8,  'Orangensaft',  0),
(9,  'Bananensaft',  0),
(10, 'Ananassaft',   0),
(11, 'Tonic Water',  0),
(12, 'Fanta',        0),
(13, 'Sprite',       0);

-- Cocktails (Beispiel)
INSERT INTO Cocktail (Name, Beschreibung, ExtLink, Bild) VALUES
('Vodka Sunrise', 'Vodka mit Orangensaft', 'example.com/vs', NULL),
('Gin Tonic',     'Gin mit Tonic Water',   'example.com/gt', NULL);

-- Rezepte
INSERT INTO Rezept (CocktailID, ZutatID, RezeptPos, Menge) VALUES
(1, 1, 1, 40),  -- Vodka Sunrise: Vodka
(1, 8, 2, 100), -- Vodka Sunrise: Orangensaft
(2, 6, 1, 40),  -- Gin Tonic: Gin
(2, 11, 2, 100);-- Gin Tonic: Tonic Water
