#!/bin/bash
set -e

# Wait for PostgreSQL to start
until pg_isready -U ${POSTGRES_USER} -d ${POSTGRES_DB}; do
  sleep 1
done


# Restore the dvdrental database
pg_restore -U ${POSTGRES_USER} -d ${POSTGRES_DB} /docker-entrypoint-initdb.d/dvdrental.tar

echo "dvdrental database restored successfully!"