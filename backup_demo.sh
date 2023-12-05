#!/bin/bash


CONTAINER_NAME="load_into_gnuhealth-postgres-1"
DATABASE_NAME="ghs"
OUTPUT_FOLDER="/home/paula/Documentos/opendx28/gnu-health-server-docker"
OUTPUT_FILE="demo.sql.gz"
PG_USER="gnuhealth"
PG_PASSWORD="gnuhealth"

# Backup and compress
docker exec $CONTAINER_NAME pg_dump -U $PG_USER -d $DATABASE_NAME | gzip > $OUTPUT_FOLDER/$OUTPUT_FILE

echo "Backup completed and saved to $OUTPUT_FOLDER/$OUTPUT_FILE"
