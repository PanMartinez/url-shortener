\echo 'Running custom initialization script...'

CREATE ROLE shortenerurl WITH LOGIN PASSWORD 'shortenerurl';
ALTER ROLE shortenerurl CREATEDB;
GRANT ALL PRIVILEGES ON DATABASE shortenerurl TO shortenerurl;
