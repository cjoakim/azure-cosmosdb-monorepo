namespace CJoakim.Cosmos
{

    using System;
    using System.Collections.Generic;
    using System.Globalization;
    using System.IO;
    using CsvHelper;
    using CsvHelper.Configuration;
    using Newtonsoft.Json;

    // Class FileUtil implements IO operations for local data files.
    // Chris Joakim, Microsoft, 2021/04/19

    public class FileUtil
    {
        public FileUtil()
        {
            // Default constructor
        }

        public string CurrentDirectory()
        {
            return Directory.GetCurrentDirectory();
        }

        public char PathSeparator()
        {
           return Path.DirectorySeparatorChar; 
        }

        public string AbsolutePath(string relativeFilename)
        {
            return CurrentDirectory() + PathSeparator() + relativeFilename;
        }

        public List<Airport> ReadAirportsCsv()
        {
            List<Airport> airports = new List<Airport>();
            try {
                string infile = AbsolutePath("data/airports/openflights_airports.csv");
                Console.WriteLine("ReadAirportsCsv: {0}", infile);

                // AirportId,Name,City,Country,IataCode,IcaoCode,Latitude,Longitude,Altitude,TimezoneNum,Dst,TimezoneCode
                // 1,"Goroka","Goroka","Papua New Guinea","GKA","AYGA",-6.081689,145.391881,5282,10,"U","Pacific/Port_Moresby"
                // 2,"Madang","Madang","Papua New Guinea","MAG","AYMD",-5.207083,145.7887,20,10,"U","Pacific/Port_Moresby"

                var config = new CsvConfiguration(CultureInfo.InvariantCulture)
                {
                    HasHeaderRecord = true,
                    HeaderValidated = null,
                    MissingFieldFound = null,
                    IgnoreBlankLines = true
                };

                using (var reader = new StreamReader(infile))
                using (var csv = new CsvReader(reader, config))
                {
                    csv.Context.RegisterClassMap<AirportMap>();
                    var records = csv.GetRecords<Airport>();
                    IEnumerable<Airport> rows = csv.GetRecords<Airport>();
                    foreach (var a in rows)
                    {
                        a.postParse();
                        if (a.IsValid())
                        {
                            airports.Add(a);
                        }
                    }
                }
            }
            catch (Exception e) {
                Exception baseException = e.GetBaseException();
                Console.WriteLine("Error in ReadAirportsCsv: {0}, Message: {1}", e.Message, baseException.Message);
            }
            return airports;
        }
    }
}
