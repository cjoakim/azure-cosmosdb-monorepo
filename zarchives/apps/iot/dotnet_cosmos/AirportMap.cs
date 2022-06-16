
using CsvHelper.Configuration;

// Mapping class for use with the CsvHelper library; maps csv header to object names.
// See https://joshclose.github.io/CsvHelper/getting-started/#reading-a-csv-file
//
// Chris Joakim, Microsoft, 2021/04/19

namespace CJoakim.Cosmos
{
    public class AirportMap : ClassMap<Airport>
    {
        public AirportMap()
        {
            // AirportId,Name,City,Country,IataCode,IcaoCode,Latitude,Longitude,Altitude,TimezoneNum,Dst,TimezoneCode 
            Map(m => m.AirportId).Name("AirportId");
            Map(m => m.Name).Name("Name");
            Map(m => m.City).Name("City");
            Map(m => m.Country).Name("Country");
            Map(m => m.IataCode).Name("IataCode");
            Map(m => m.IcaoCode).Name("IcaoCode");
            Map(m => m.Latitude).Name("Latitude");
            Map(m => m.Longitude).Name("Longitude");
            Map(m => m.Altitude).Name("Altitude");
            Map(m => m.TimezoneNum).Name("TimezoneNum");
            Map(m => m.Dst).Name("Dst");
            Map(m => m.TimezoneCode).Name("TimezoneCode");
        }
    }
}