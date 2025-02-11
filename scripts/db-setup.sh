#!/bin/sh

export PGUSER="postgres"

psql -c "CREATE DATABASE books"

psql books -c "CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\";"
