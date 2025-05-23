-- BarbotDB: Table Definitions

CREATE TABLE IF NOT EXISTS Cocktail (
    CocktailID INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(30),
    Beschreibung VARCHAR(250),
    ExtLink VARCHAR(200),
    Bild BLOB
);

CREATE TABLE IF NOT EXISTS Zapfstelle (
    ZapfstelleID INT AUTO_INCREMENT PRIMARY KEY,
    SchienenPos INT,
    Pumpe TINYINT,
    PumpenNR INT,
    Fuellmenge INT
);

CREATE TABLE IF NOT EXISTS Zutat (
    ZutatID INT AUTO_INCREMENT PRIMARY KEY,
    Zapfstelle INT,
    Name VARCHAR(30),
    Alkohol TINYINT,
    FOREIGN KEY (Zapfstelle) REFERENCES Zapfstelle(ZapfstelleID)
);

CREATE TABLE IF NOT EXISTS Rezept (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    CocktailID INT,
    ZutatID INT,
    RezeptPos INT,
    Menge INT,
    FOREIGN KEY (CocktailID) REFERENCES Cocktail(CocktailID),
    FOREIGN KEY (ZutatID) REFERENCES Zutat(ZutatID)
);

-- 1. Insert Cocktails (no dependencies)
INSERT INTO Cocktail (Name, Beschreibung, ExtLink, Bild) VALUES
('Vodka Sunrise', 'Vodka mit Orangensaft', 'https://example.com/vodka-sunrise', NULL),
('Gin Tonic',     'Gin mit Tonic Water',   'https://example.com/gin-tonic', NULL),
('Bacardi Cola',  'Bacardi mit Cola',      'https://example.com/bacardi-cola', NULL),
('Tequila Fanta', 'Tequila mit Fanta',     'https://example.com/tequila-fanta', NULL),
('Korn Sprite',   'Korn mit Sprite',       'https://example.com/korn-sprite', NULL);

-- 2. Insert Zapfstelle (no dependencies)
INSERT INTO Zapfstelle (SchienenPos, Pumpe, PumpenNR, Fuellmenge) VALUES
(25,    0, NULL, 1000),   -- 1: Vodka (servo)
(525,   0, NULL, 1000),   -- 2: Tequila (servo)
(1025,  0, NULL, 1000),   -- 3: Bacardi (servo)
(1525,  0, NULL, 1000),   -- 4: Rum (servo)
(2025,  0, NULL, 1000),   -- 5: Korn (servo)
(2525,  0, NULL, 1000),   -- 6: Gin (servo)
(3025,  1, 0,    1000),   -- 7: Cola (pump)
(3025,  1, 1,    1000),   -- 8: Orangensaft (pump)
(3025,  1, 2,    1000),   -- 9: Bananensaft (pump)
(3025,  1, 3,    1000),   -- 10: Ananassaft (pump)
(3025,  1, 4,    1000),   -- 11: Tonic Water (pump)
(3025,  1, 5,    1000),   -- 12: Fanta (pump)
(3025,  1, 6,    1000);   -- 13: Sprite (pump)

-- 3. Insert Zutat (references Zapfstelle)
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

-- 4. Insert Rezept (references Cocktail and Zutat)
INSERT INTO Rezept (CocktailID, ZutatID, RezeptPos, Menge) VALUES
(1, 1, 1, 40),   -- Vodka Sunrise: Vodka
(1, 8, 2, 100),  -- Vodka Sunrise: Orangensaft
(2, 6, 1, 40),   -- Gin Tonic: Gin
(2, 11, 2, 100), -- Gin Tonic: Tonic Water
(3, 3, 1, 40),   -- Bacardi Cola: Bacardi
(3, 7, 2, 100),  -- Bacardi Cola: Cola
(4, 2, 1, 40),   -- Tequila Fanta: Tequila
(4, 12, 2, 100), -- Tequila Fanta: Fanta
(5, 5, 1, 40),   -- Korn Sprite: Korn
(5, 13, 2, 100); -- Korn Sprite: Sprite
