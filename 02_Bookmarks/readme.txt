docker stop <container_id>
docker rm <container_id>
rm -rf /Users/oleksandrkharchenko/Documents/DataBases/postgres/*


docker run \
  --name postgres_clean \
  -e POSTGRES_PASSWORD=8lyrMibko \
  -e PGDATA=/var/lib/postgresql/data/pgdata \
  -v /Users/oleksandrkharchenko/Documents/DataBases/postgres:/var/lib/postgresql/data \
  -p 5432:5432 \
  -d postgres


  python manage.py runserver_plus --cert-file cert.crt