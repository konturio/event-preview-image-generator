#!/bin/sh
docker-compose --project-name test-epig --env-file tests/.env -f ./docker-compose.yml -f tests/docker-compose.test.yml up