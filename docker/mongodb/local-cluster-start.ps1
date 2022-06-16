

# PowerShell script to start a localhost mongodb cluster with Docker.
# Chris Joakim, Microsoft

echo 'create mongoClusterNetwork ...'
docker network create mongoClusterNetwork

echo 'start mongo1 ...'
docker run -d --rm -p 27017:27017 --name mongo1 --network mongoClusterNetwork mongo:5 mongod --replSet localRS --bind_ip localhost,mongo1

echo 'start mongo2 ...'
docker run -d --rm -p 27018:27017 --name mongo2 --network mongoClusterNetwork mongo:5 mongod --replSet localRS --bind_ip localhost,mongo2

echo 'start mongo3 ...'
docker run -d --rm -p 27019:27017 --name mongo3 --network mongoClusterNetwork mongo:5 mongod --replSet localRS --bind_ip localhost,mongo3

echo 'initiate the cluster ...'
docker exec -it mongo1 mongosh --eval "rs.initiate({_id: 'localRS', members: [ {_id: 0, host: 'mongo1'}, {_id: 1, host: 'mongo2'}, {_id: 2, host: 'mongo3'} ]})"

echo 'list running containers ...'
docker ps
