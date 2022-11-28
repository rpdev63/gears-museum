CREATE TABLE IF NOT EXISTS user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS gear (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name VarChar(80) NOT NULL,
  image TEXT,
  description TEXT,
  advantages TEXT,
  disadvantages TEXT,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  author_id INTEGER NOT NULL,
  FOREIGN KEY (author_id) REFERENCES user (id)
);

CREATE TABLE IF NOT EXISTS post (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id INTEGER NOT NULL,
  gear_id INTEGER DEFAULT 0,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  title TEXT NOT NULL,
  body TEXT NOT NULL,
  FOREIGN KEY (author_id) REFERENCES user (id),
  FOREIGN KEY (gear_id) REFERENCES gear(id)
);

INSERT INTO user (username, password)
VALUES 
('admin1', 'FgregDFnf'),
('user1', 'Ufzojvrehhtrf');

INSERT INTO gear (name, image, description, advantages, disadvantages, author_id)
VALUES 
(
'engrenages cylindriques à denture droite', 
NULL, 
'Cet engrenage peut-être de deux types, extérieur ou intérieur', 
'simple et économique', 
'bruyant et vitesses de rotation limitées',  
1
),
(
'engrenages cylindriques à denture hélicoïdale', 
NULL, 
'Pour les machines outils', 
'transmission plus souple et moins bruyante, vitesses plus importantes', 
'effort axial supplémentaire, rendement moins bon', 
1
),
(
'engrenages coniques', 
NULL, 
'Réalisé sur tailleuse à couteaux', 
'possibilité de choisir le sens de rotation de la roue menée', 
'solution moins économique, nécessite un réglage des roues au montage', 
2
),
(
'engrenages à roue et vis sans fin', 
NULL, 
'modèle bronze, entrées pour arcellormittal', 
'arbres quelconques, souvent orthogonaux', 
'rendement faible et parfois non réversible (ce qui peut être aussi un avantage)', 
2
);

INSERT INTO post (title, body, author_id, gear_id)
VALUES 
('Premier post', 'Présentation du premier engrenage', 1, 1),
('Deuxième post', 'Présentation pour les autres engrenages', 1, 2),
('Autre poste', 'Encore un autre engrenage pour alimenter les ressources', 2, 2);


