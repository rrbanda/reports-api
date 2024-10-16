# app/init-mongo/init.sh

#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Wait for MongoDB to be ready
echo "Waiting for MongoDB to be ready..."
until mongo --host localhost --port 27017 --eval "print(\"waited for connection\")"
do
    sleep 1
done

# Import patient data
echo "Importing patient data..."
mongoimport --db patient_db --collection patients --file /docker-entrypoint-initdb.d/patient_data.json --jsonArray

echo "Patient data imported successfully."
