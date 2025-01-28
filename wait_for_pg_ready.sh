#!/bin/bash

# Function to check if PostgreSQL is up and running
check_postgres() {
  pg_isready -q
}

# Loop until PostgreSQL is ready
until check_postgres; do
  echo "Waiting for PostgreSQL to start..."
  sleep 2
done
