#!/bin/bash


set -e

if [ -v PASSWORD_FILE ]; then
    PASSWORD="$(< $PASSWORD_FILE)"
fi

# set the postgres database host, port, user and password according to the environment
# and pass them as arguments to the odoo process if not present in the config file
: ${HOST:=${DB_PORT_5432_TCP_ADDR:='db'}}
: ${PORT:=${DB_PORT_5432_TCP_PORT:=5432}}
: ${USER:=${DB_ENV_POSTGRES_USER:=${POSTGRES_USER:='odoo'}}}
: ${PASSWORD:=${DB_ENV_POSTGRES_PASSWORD:=${POSTGRES_PASSWORD:='odoo'}}}

# add command args
DB_ARGS=()
function check_config() {
    param="$1"
    value="$2"
    if grep -q -E "^\s*\b${param}\b\s*=" "$ODOO_RC" ; then
        value=$(grep -E "^\s*\b${param}\b\s*=" "$ODOO_RC" |cut -d " " -f3|sed 's/["\n\r]//g')
    fi;
    DB_ARGS+=("--${param}")
    DB_ARGS+=("${value}")
}
check_config "db_host" "$HOST"
check_config "db_port" "$PORT"
check_config "db_user" "$USER"
check_config "db_password" "$PASSWORD"

wait-for-psql.py ${DB_ARGS[@]} --timeout=30

check_config "database" "$DATABASE"
check_config "db-filter" "$DATABASE"
check_config "dev" "all"
check_config "log-handler" "odoo.tools.convert:DEBUG"

if [[ "$INIT_DATABASE" == "Y" ]] ; then
    check_config "init" "base"
fi;

if [[ "$UPDATE" == "Y" ]] ; then
    check_config "update" "$MODULES"
fi;

case "$1" in
    -- | odoo)
        shift
        if [[ "$1" == "scaffold" ]] ; then
            exec odoo "$@"
        else
            echo "Run Odoo..."
            exec odoo "$@" "${DB_ARGS[@]}"
        fi
        ;;
    debug)
        echo "Run Odoo in Debug Mode..."
        exec /usr/bin/python3 -m debugpy --wait-for-client --listen 0.0.0.0:5678 /usr/bin/odoo "${DB_ARGS[@]}"
        ;;
    -*)
        echo "Run Odoo..."
        exec odoo "$@" "${DB_ARGS[@]}"
        ;;
    *)
        echo "Run Odoo..."
        exec "$@"
esac

exit 1
