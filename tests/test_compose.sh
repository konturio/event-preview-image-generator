#!/bin/sh
docker-compose --project-name test-epig --env-file .env -f ../docker-compose.yml -f docker-compose.test.yml up