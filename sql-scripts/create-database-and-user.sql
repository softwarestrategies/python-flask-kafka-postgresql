CREATE
DATABASE pfkp;

CREATE
USER pfkp_admin with encrypted password 'changeme';
GRANT ALL PRIVILEGES ON DATABASE
pfkp to pfkp_admin;
