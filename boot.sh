#!/bin/bash
# this script is used to boot a Docker container
while true; do
    flask db upgrade
    if [[ "$?" == "0" ]]; then
        break
    fi
    echo Deploy command failed, retrying in 5 seconds...
    sleep 5
done
echo "Creating admin user..."
python -m flask db_inits create_admin william.b.hemingway@gmail.com --username william.b.hemingway
echo "Starting Gunicorn server..."
exec gunicorn -b :5000 --access-logfile - --error-logfile - milliavod:app