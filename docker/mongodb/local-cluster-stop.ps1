

# PowerShell script to start a localhost mongodb cluster with Docker.
# Chris Joakim, Microsoft

echo 'listing the running containers ...'
docker ps
docker ps -q 

echo 'stopping the running containers ...'
docker stop $(docker ps -q)

echo 'listing docker networks ...'
docker network ls

echo 'pruning docker networks ...'
docker network prune --force

echo 'listing docker networks after pruning ...'
docker network ls

echo 'listing running containers ...'
docker ps
