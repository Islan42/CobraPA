DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS cidade;
DROP TABLE IF EXISTS ticket;
DROP TABLE IF EXISTS promocao;

CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    adm INTEGER NOT NULL
);

CREATE TABLE cidade (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    promocao_id INTEGER,
    FOREIGN KEY (promocao_id) REFERENCES promocao (id)
);

CREATE TABLE ticket (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    origem_id INTEGER NOT NULL,
    destino_id INTEGER NOT NULL,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    partida TIMESTAMP NOT NULL,
    FOREIGN KEY (user_id) REFERENCES user (id),
    FOREIGN KEY (origem_id) REFERENCES cidade (id),
    FOREIGN KEY (destino_id) REFERENCES cidade (id)
);

CREATE TABLE promocao (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    desconto INTEGER NOT NULL,
    ativo INTEGER NOT NULL,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);