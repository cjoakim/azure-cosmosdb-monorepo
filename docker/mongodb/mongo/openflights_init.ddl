// MongoDB "DDL" initialize the "openflights" database and its collections.
// Chris Joakim, Microsoft

use OpenFlights

db.Airports.drop()
db.Airlines.drop()
db.Countries.drop()
db.Planes.drop()
db.Routes.drop()
db.Passengers.drop()

db.createCollection("Airports")
db.createCollection("Airlines")
db.createCollection("Countries")
db.createCollection("Planes")
db.createCollection("Routes")
db.createCollection("Passengers")

show collections
