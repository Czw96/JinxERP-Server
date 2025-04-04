#!/bin/sh

python manage.py migrate_schemas

exec "$@"
