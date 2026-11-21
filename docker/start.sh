#!/бин/ш
set -e
service cron start
exec python /opt/maltrail/server.py