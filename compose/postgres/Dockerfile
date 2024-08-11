FROM postgres:16.3
COPY init.sql /docker-entrypoint-initdb.d
CMD ["docker-entrypoint.sh", "postgres"]
