#!/bin/bash

_rootdir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"


if nc -z localhost 5432
then
  clear
  echo "Database was already running..."
else
  echo "Starting database..."
  cd $_rootdir/compose/odoo15_db
  docker-compose down && docker-compose -p odoo15_db up -d
fi

echo ""
while ! nc -z localhost 5432
do
  printf "."
  sleep 0.1
done

cd $_rootdir/compose/odoo15_app
docker-compose down
docker-compose -p odoo15_app --env-file .env-debug up &

echo ""
while ! nc -z localhost 5678
do
  printf "."
  sleep 0.1
done

echo ""
echo "Wait for debug server..."
sleep 5

exit 0
