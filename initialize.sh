DB_NAME="Exam"
DB_USER="Alla"
DB_PASSWORD="2002"
DB_OWNER="Alla"

sudo -u postgres psql -c "DROP USER IF EXISTS $DB_USER;"

sudo -u postgres psql -c "CREATE USER $DB_USER WITH PASSWORD '$DB_PASSWORD';"

sudo -u postgres psql -c "ALTER DATABASE $DB_NAME OWNER TO $DB_OWNER;"
