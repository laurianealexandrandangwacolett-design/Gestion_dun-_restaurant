DROP TABLE IF EXISTS plats;
DROP TABLE IF EXISTS reservations;

CREATE TABLE plats (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT NOT NULL,
    categorie TEXT NOT NULL,
    prix INTEGER NOT NULL CHECK (prix > 0)
);

CREATE TABLE reservations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT NOT NULL,
    telephone TEXT NOT NULL,
    date TEXT NOT NULL,
    service TEXT NOT NULL CHECK (service IN ('midi', 'soir')),
    personnes INTEGER NOT NULL CHECK (personnes BETWEEN 1 AND 20),
    cree_le TEXT DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO plats (nom, categorie, prix) VALUES
('Beignets haricots', 'entree', 1000),
('Ndolé aux crevettes', 'plat', 4000),
('Poulet DG', 'plat', 4500),
('Poisson braisé', 'plat', 5000),
('Eru', 'plat', 3500),
('Jus de foléré', 'boisson', 500),
('Jus de gingembre', 'boisson', 500);