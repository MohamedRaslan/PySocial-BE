#!/bin/bash
set -e

# Wait for PostgreSQL to start
until pg_isready -U ${DB_USERNAME} -d ${DB_NAME}; do
  sleep 1
done


# Restore the dvdrental database
pg_restore -U ${DB_USERNAME} -d ${DB_NAME} /docker-entrypoint-initdb.d/dvdrental.tar

echo "dvdrental database restored successfully!"