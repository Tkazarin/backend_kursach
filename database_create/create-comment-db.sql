USE backend_kursach;

DROP TABLE IF EXISTS comment;

CREATE TABLE comment (
    id_comment INT AUTO_INCREMENT PRIMARY KEY,
    id_user INT NOT NULL,
    id_fic INT NOT NULL,
    text TEXT,
    published DATETIME,
    FOREIGN KEY (id_user) REFERENCES user(id_user),
    FOREIGN KEY (id_fic) REFERENCES fic(id_fic)
);