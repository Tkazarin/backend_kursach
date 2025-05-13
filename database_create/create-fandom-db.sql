USE backend_kursach;

DROP TABLE IF EXISTS fandom;

CREATE TABLE fandom (
    id_fandom INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL UNIQUE,
    description VARCHAR(255),
    type VARCHAR(255)
);