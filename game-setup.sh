#!/bin/bash

docker exec -i vizsciflowdb psql -U phenodoop -d biowl < gamification.sql

