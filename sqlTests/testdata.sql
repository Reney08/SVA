-- Zapfstelle
INSERT INTO Zapfstelle (SchienenPos, Pumpe, PumpenNR) VALUES
  (1, 1, 101),
  (2, 0, 102),
  (3, 1, 103);

-- Zutat
INSERT INTO Zutat (Name, Zapfstelle) VALUES
  ('Rum', 1),
  ('Minze', 2),
  ('Limette', 2),
  ('Zucker', 3),
  ('Soda', 1),
  ('Cachaça', 1),
  ('Gin', 1),
  ('Tonic Water', 3);

-- Cocktail
INSERT INTO Cocktail (Name, Beschreibung, LINK) VALUES
  ('Mojito', 'Ein erfrischender kubanischer Cocktail mit Minze und Limette.', 'https://example.com/mojito'),
  ('Caipirinha', 'Brasilianischer Cocktail mit Limette und Cachaça.', 'https://example.com/caipirinha'),
  ('Gin Tonic', 'Klassischer Longdrink mit Gin und Tonic Water.', 'https://example.com/gin-tonic');

-- Rezept
INSERT INTO Rezept (CocktailID, RezeptPos, ZutatID, Menge) VALUES
  (1, 1, 1, 4),  -- Mojito: Rum
  (1, 2, 2, 6),  -- Mojito: Minze
  (1, 3, 3, 2),  -- Mojito: Limette
  (1, 4, 4, 2),  -- Mojito: Zucker
  (1, 5, 5, 8),  -- Mojito: Soda

  (2, 1, 6, 5),  -- Caipirinha: Cachaça
  (2, 2, 3, 2),  -- Caipirinha: Limette
  (2, 3, 4, 2),  -- Caipirinha: Zucker

  (3, 1, 7, 4),   -- Gin Tonic: Gin
  (3, 2, 8, 10);  -- Gin Tonic: Tonic Water
