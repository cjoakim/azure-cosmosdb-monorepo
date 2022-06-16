using System;
using System.Threading;
using System.Threading.Tasks;
using System.Collections.Generic;
using Microsoft.Azure.Cosmos;


// Program entry point, invoked from the command-line.
// Chris Joakim, Microsoft, 2021/04/19

namespace CJoakim.Cosmos
{
    class Program  {

        private static string[] programArgs = null;
        private static int      argCount = 0;

        public static async Task Main(string[] args)
        { 

            try {
                programArgs = args;
                argCount = programArgs.Length;

                int argc = args.Length;
                if (argCount > 0)
                {
                    string f = programArgs[0];
                    string dbname = null;
                    string cname = null;
                    string pk = null;
                    string id = null;
                    int maxCount;
                    int limit;
                    int pauseMs;
                    double lat;
                    double lng;
                    double meters;
                    double startEpoch;
                    double endEpoch;

                    switch (programArgs[0])
                    {
                        case "upsertAirports":
                            maxCount = Int32.Parse(programArgs[1]);
                            pauseMs  = Int32.Parse(programArgs[2]);
                            await upsertAirports(maxCount, pauseMs);
                            break;

                        case "queryAirportsByPk":
                            pk = programArgs[1].ToUpper();
                            await queryAirportsByPk(pk);
                            break;

                        case "queryAirportsByPkId":
                            pk = programArgs[1].ToUpper();
                            id = programArgs[2];
                            await queryAirportsByPkId(pk, id);
                            break;

                        case "queryAirportsByGPS":
                            lng = Double.Parse(programArgs[1]);
                            lat = Double.Parse(programArgs[2]);
                            meters = Double.Parse(programArgs[3]);
                            await queryAirportsByGPS(lng, lat, meters);
                            break;

                        case "queryEvents":
                            startEpoch = Double.Parse(programArgs[1]);
                            endEpoch = Double.Parse(programArgs[2]);
                            await queryEvents(startEpoch, endEpoch);
                            break;

                        case "queryLatestEvents":
                            limit = Int32.Parse(programArgs[1]);
                            await queryLatestEvents(limit);
                            break;

                        case "deleteDocuments":
                            dbname = programArgs[1];
                            cname = programArgs[2];
                            maxCount = Int32.Parse(programArgs[3]);
                            await deleteDocuments(dbname, cname, maxCount);
                            break;

                        case "displayRegions":
                            Console.WriteLine("Displayng the values of a few Regions...");
                            Console.WriteLine($"Regions.EastUS:   {Regions.EastUS}");
                            Console.WriteLine($"Regions.EastUS2:  {Regions.EastUS2}");
                            Console.WriteLine($"Regions.WestUS:   {Regions.WestUS}");
                            Console.WriteLine($"Regions.WestUS2:  {Regions.WestUS2}");
                            Console.WriteLine($"Regions.EastAsia: {Regions.EastAsia}");
                            string regionsEnv = Environment.GetEnvironmentVariable("AZURE_IOT_COSMOSDB_SQLDB_PREF_REGIONS");
                            Console.WriteLine($"Your env var regions: {regionsEnv}");
                            break;

                        default:
                            log("undefined command-line function: " + programArgs[0]);
                            displayUsage();
                            break;
                    }
                }
                else
                {
                    displayUsage();
                }
            }
            catch (Exception e) {
                Console.WriteLine(e);
                Console.WriteLine(e.Message);
            }
            await Task.Delay(10);
        }

        static async Task upsertAirports(int maxCount, int pauseMs)
        {
            log($"upsertAirports: {maxCount}  pauseMs: {pauseMs}");

            FileUtil fsu = new FileUtil();
            List<Airport> airports = new FileUtil().ReadAirportsCsv();
            log($"airports read from csv file: {airports.Count}");

            CosmosUtil cu = new CosmosUtil();
            string dbname = Environment.GetEnvironmentVariable("AZURE_IOT_COSMOSDB_SQLDB_DBNAME");
            string cname  = Environment.GetEnvironmentVariable("AZURE_IOT_COSMOSDB_SQLDB_COLLNAME");
            await cu.setCurrentDatabase(dbname);
            await cu.setCurrentContainer(cname);

            for (int i = 0; i < airports.Count; i++)
            {
                if (i < maxCount) {
                    Airport a = airports[i];
                    a.UpdateEpoch();
                    log("===");
                    Console.WriteLine(a.ToJson());
                    ItemResponse<Airport> response = await cu.upsertAirportDocument(a);
                    log("---");
                    log($"status code:    {response.StatusCode}");
                    log($"request charge: {response.RequestCharge}");
                    //log($"diagnostics:    {response.Diagnostics}");
                    //log($"resource:       {response.Resource}");
                    Thread.Sleep(pauseMs);
                }
            }
            log($"airports read from csv file: {airports.Count}");
            return;
        }

        static async Task queryEvents(double startEpoch, double endEpoch)
        {
            log($"queryEvents: {startEpoch} to {endEpoch}");

            CosmosUtil cu = new CosmosUtil();
            string dbname = Environment.GetEnvironmentVariable("AZURE_IOT_COSMOSDB_SQLDB_DBNAME");
            string cname = "events";
            await cu.setCurrentDatabase(dbname);
            await cu.setCurrentContainer(cname);
            string sql = $"select * from c where c.epoch >= {startEpoch} and c.epoch < {endEpoch}";

            List<dynamic> items = await cu.queryDocuments(sql);

            for (int i = 0; i < items.Count; i++)
            {
                Console.WriteLine(items[i]);
            }
            return;
        }

        static async Task queryLatestEvents(int limit)
        {
            log("queryLatestEvents");

            CosmosUtil cu = new CosmosUtil();
            string dbname = Environment.GetEnvironmentVariable("AZURE_IOT_COSMOSDB_SQLDB_DBNAME");
            string cname = "events";
            await cu.setCurrentDatabase(dbname);
            await cu.setCurrentContainer(cname);
            string sql = $"select * from c order by c.epoch desc offset 0 limit {limit}";

            List<dynamic> items = await cu.queryDocuments(sql);

            for (int i = 0; i < items.Count; i++)
            {
                Console.WriteLine(items[i]);
            }
            return;
        }

        static async Task queryAirportsByPk(string pk)
        {
            log("queryAirportsByPk");
            CosmosUtil cu = new CosmosUtil();
            string dbname = Environment.GetEnvironmentVariable("AZURE_IOT_COSMOSDB_SQLDB_DBNAME");
            string cname = "airports";
            await cu.setCurrentDatabase(dbname);
            await cu.setCurrentContainer(cname);
            string sql = $"select * from c where c.pk = '{pk}'";

            List<dynamic> items = await cu.queryDocuments(sql);

            for (int i = 0; i < items.Count; i++)
            {
                Console.WriteLine(items[i]);
            }
            return;
        }

        static async Task queryAirportsByPkId(string pk, string id)
        {
            log("queryAirportsByPkId");
            CosmosUtil cu = new CosmosUtil();
            string dbname = Environment.GetEnvironmentVariable("AZURE_IOT_COSMOSDB_SQLDB_DBNAME");
            string cname = "airports";
            await cu.setCurrentDatabase(dbname);
            await cu.setCurrentContainer(cname);
            string sql = $"select * from c where c.pk = '{pk}' and c.id = '{id}'";

            List<dynamic> items = await cu.queryDocuments(sql);

            for (int i = 0; i < items.Count; i++)
            {
                Console.WriteLine(items[i]);
            }
            return;
        }

        static async Task queryAirportsByGPS(double lng, double lat, double meters)
        {
            log("queryAirportsByGPS");
            CosmosUtil cu = new CosmosUtil();
            string dbname = Environment.GetEnvironmentVariable("AZURE_IOT_COSMOSDB_SQLDB_DBNAME");
            string cname = "airports";
            await cu.setCurrentDatabase(dbname);
            await cu.setCurrentContainer(cname);
            string location = $"[{lng}, {lat}]";
            string sql = "select c.pk, c.Name, c.City, c.location.coordinates from c " +
                         "where ST_DISTANCE(c.location, { \"type\": \"Point\", \"coordinates\":" +
                          location + "}) < " + meters;

            List<dynamic> items = await cu.queryDocuments(sql);

            for (int i = 0; i < items.Count; i++)
            {
                Console.WriteLine(items[i]);
            }
            return;
        }

        static async Task deleteDocuments(string dbname, string cname, int maxCount)
        {
            log($"deleteDocuments; db: {dbname}, container: {cname}, maxCount: {maxCount}");

            CosmosUtil cu = new CosmosUtil();
            await cu.setCurrentDatabase(dbname);
            await cu.setCurrentContainer(cname);

            string sql = $"select * from c";
            List<dynamic> items = await cu.queryDocuments(sql, maxCount);

            log($"deleteDocuments, count: {items.Count}");
            for (int i = 0; i < items.Count; i++)
            {
                Console.WriteLine(items[i]);
                log($"deleting item: {items[i].id}, {items[i].pk}");
                string id = items[i].id;
                string pk = items[i].pk;
                GenericDocument doc = new GenericDocument();
                doc.id = items[i].id;
                doc.pk = items[i].pk;

                ItemResponse<GenericDocument> response = await cu.deleteGenericDocument(doc);
                log($"status code:    {response.StatusCode}");
                log($"request charge: {response.RequestCharge}");
            }
        }

        private static void displayUsage()
        {
            log("Usage:");
            log("dotnet run upsertAirports <maxCount> <pauseMs>");
            log("dotnet run queryAirportsByPk <pk>");
            log("dotnet run queryAirportsByPk TPA");
            log("dotnet run queryAirportsByPkId TPA c49d4114-f804-4db8-8628-647b45ac9f27");
            log("dotnet run queryAirportsByGPS <latitude> <longitude> <meters>");
            log("dotnet run queryAirportsByGPS -80.848481 35.499254 30000.0 Davidson, NC");
            log("dotnet run queryAirportsByGPS -82.648830 27.867174 10000.0 St. Petersburg, FL");
            log("dotnet run queryLatestEvents <limit>");
            log("dotnet run queryLatestEvents 3");
            log("dotnet run queryEvents <startEpoch> <endEpoch>");
            log("dotnet run queryEvents 1604330634 1604330643");
            log("dotnet run deleteDocuments <dbname> <cname> <maxCount>");
            log("dotnet run deleteDocuments dev airports 99999");
            log("dotnet run displayRegions");
        }

        private static void log(String msg)
        {
            Console.WriteLine("" + msg);
        } 
    }
}
