USE backend_kursach;

DROP TABLE IF EXISTS fic;

CREATE TABLE fic (
    id_fic INT AUTO_INCREMENT PRIMARY KEY,
    id_user INT NOT NULL,
    id_fandom INT NOT NULL,
    title VARCHAR(255) NOT NULL UNIQUE,
    description TEXT,
    text TEXT,
    likes INT DEFAULT 0,
    published DATETIME,
    FOREIGN KEY (id_user) REFERENCES user(id_user),
    FOREIGN KEY (id_fandom) REFERENCES fandom(id_fandom)
);