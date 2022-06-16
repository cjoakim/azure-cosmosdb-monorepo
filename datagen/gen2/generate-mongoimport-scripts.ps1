
# Generate the mongoimport scripts which use the generated JSON data.
# Chris Joakim, Microsoft, May 2022
#
# See https://www.mongodb.com/docs/atlas/import/mongoimport/
#
# Examples:
# mongodb://root:<PASSWORD>@atlas-host1:27017
# mongodb://127.0.0.1:27017
# mongodb://root:rootpassword@127.0.0.1:27017
# mongodb://@localhost:27017

python main.py generate_mongoimport_scripts mongodb://@localhost:27017 dev --nossl ps1

python main.py generate_mongoimport_scripts mongodb://@localhost:27017 dev --nossl sh

echo 'done'
