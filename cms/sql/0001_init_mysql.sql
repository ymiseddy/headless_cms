CREATE TABLE migrations (
    migration_id INTEGER NOT NULL AUTO_INCREMENT PRIMARY KEY,
    filename VARCHAR(50) NOT NULL,
    processed DATETIME NOT NULL
);
INSERT INTO migrations (filename, processed) VALUES ("001_init_mysql.sql", NOW());



CREATE TABLE users
(
    user_id    INTEGER NOT NULL AUTO_INCREMENT PRIMARY KEY,
    entity_id  VARCHAR(28),
    email      VARCHAR(35),
    first_name VARCHAR(20),
    last_name  VARCHAR(20),
    CONSTRAINT uq_users_email UNIQUE (email),
    CONSTRAINT uq_users_entity_id UNIQUE (entity_id)
);

CREATE TABLE clients (
    client_id INTEGER NOT NULL AUTO_INCREMENT PRIMARY KEY,
    entity_id VARCHAR(28),
    name VARCHAR(60),
    CONSTRAINT uq_clients_entity UNIQUE(entity_id)
);

CREATE TABLE articles (
    article_id INTEGER NOT NULL AUTO_INCREMENT PRIMARY KEY,
    entity_id VARCHAR(28),
    title VARCHAR(80),
    author VARCHAR(45),
    summary TEXT,
    CONSTRAINT uq_articles_entity UNIQUE(entity_id)
);