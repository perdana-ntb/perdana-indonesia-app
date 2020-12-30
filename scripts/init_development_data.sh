#!/bin/bash

echo "Apply database migrations"
python manage.py migrate

echo "Generate user groups"
python manage.py generate_groups

echo "Generate region data"
python manage.py generate_region_data

echo "Generate fake organisation data"
python manage.py generate_organisations
