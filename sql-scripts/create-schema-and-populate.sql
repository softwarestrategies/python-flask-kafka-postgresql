CREATE TABLE project
(
    id          SERIAL PRIMARY KEY,
    created_on  TIMESTAMP DEFAULT now() NOT NULL,
    modified_on TIMESTAMP DEFAULT now() NOT NULL,
    name        VARCHAR(50)             NOT NULL,
    description VARCHAR(255)            NOT NULL,
    status      VARCHAR(20)             NOT NULL
);
