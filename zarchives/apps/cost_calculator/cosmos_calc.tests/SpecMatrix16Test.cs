using System;
using System.Text;
using System.Text.Json;
using System.Text.Json.Serialization;

using Xunit;

using CJoakim.CosmosCalc;

// Xunit unit tests for a Specification Matrix Scenario.
// Chris Joakim, Microsoft, 2020-11-08

namespace cosmos_calc.tests
{
    public class SpecMatrix16Test
    {
        [Fact]
        public void TestSpecMatrix16Test()
        {
            Container c = new Container();
            c.name                  = "container16";
            c.provisioningType      = "autoscale";
            c.replicationType       = "single";
            c.availabilityZone      = true;
            c.regionCount           = 1;
            c.sizeInGB              = 3;
            c.replicatedGBPerMonth  = 0.0;
            c.ruPerSecond           = 400;
            c.synapseLinkEnabled    = true;
            c.maxHistoricalManualRu = 0;
            c.maxHistoricalAutoRu   = 0;

            int    expectedCalculatedMinRU             = 400;
            double expectedCalculatedRatePer100RU      = 0.015;
            double expectedCalculatedRUInHundreds      = 4;
            double expectedCalculatedRuDollarsPerHour  = 0.06;
            double expectedCalculatedRuDollarsPerMonth = 43.68;
            double expectedCalculatedEgressPerMonth    = 0;
            double expectedCalculatedStoragePerMonth   = 0.75;
            double expectedCalculatedAnalyticalStoragePerMonth = 0.06;
            double expectedCalculatedTotalPerMonth     = 44.49;

            double costs = c.CalculateCosts();
            double tolerance = 0.01;
            
            //LogContainerJson(c);

            Assert.True(c.calculatedMinRU + tolerance > expectedCalculatedMinRU);
            Assert.True(c.calculatedMinRU - tolerance < expectedCalculatedMinRU);

            Assert.True(c.calculatedRatePer100RU + tolerance > expectedCalculatedRatePer100RU);
            Assert.True(c.calculatedRatePer100RU - tolerance < expectedCalculatedRatePer100RU);
        
            Assert.True(c.calculatedRUInHundreds + tolerance > expectedCalculatedRUInHundreds);
            Assert.True(c.calculatedRUInHundreds - tolerance < expectedCalculatedRUInHundreds);

            Assert.True(c.calculatedRuDollarsPerHour + tolerance > expectedCalculatedRuDollarsPerHour);
            Assert.True(c.calculatedRuDollarsPerHour - tolerance < expectedCalculatedRuDollarsPerHour);

            Assert.True(c.calculatedRuDollarsPerMonth + tolerance > expectedCalculatedRuDollarsPerMonth);
            Assert.True(c.calculatedRuDollarsPerMonth - tolerance < expectedCalculatedRuDollarsPerMonth);

            Assert.True(c.calculatedEgressPerMonth + tolerance > expectedCalculatedEgressPerMonth);
            Assert.True(c.calculatedEgressPerMonth - tolerance < expectedCalculatedEgressPerMonth);

            Assert.True(c.calculatedStoragePerMonth + tolerance > expectedCalculatedStoragePerMonth);
            Assert.True(c.calculatedStoragePerMonth - tolerance < expectedCalculatedStoragePerMonth);

            Assert.True(c.calculatedAnalyticalStoragePerMonth + tolerance > expectedCalculatedAnalyticalStoragePerMonth);
            Assert.True(c.calculatedAnalyticalStoragePerMonth - tolerance < expectedCalculatedAnalyticalStoragePerMonth);

            Assert.True(c.calculatedTotalPerMonth + tolerance > expectedCalculatedTotalPerMonth);
            Assert.True(c.calculatedTotalPerMonth - tolerance < expectedCalculatedTotalPerMonth);
        }

        private void LogContainerJson(Container c)
        {
            var options = new JsonSerializerOptions
            {
                WriteIndented = true,
            };
            Console.WriteLine(JsonSerializer.Serialize(c, options));
        }
    }
}

/*
Azure CosmosDB Cost Calculator Specification File

container:               container16
provisioning_type:       autoscale
replication_type:        single
region_count:            1
availability_zone:       true
size_in_gb:              3
replicated_gb_per_month: 0.0
ru_per_second:           400
synapse_link_enabled:    true
calculate_costs:         true

*/

/*
{
  "name": "container16",
  "sizeInGB": 3,
  "provisioningType": "autoscale",
  "availabilityZone": true,
  "synapseLinkEnabled": true,
  "replicationType": "single",
  "regionCount": 1,
  "ruPerSecond": 400,
  "maxHistoricalManualRu": 0,
  "maxHistoricalAutoRu": 0,
  "replicatedGBPerMonth": 0,
  "calculatedMinRU": 400,
  "calculatedRatePer100RU": 0.015,
  "calculatedRUInHundreds": 4,
  "calculatedRuDollarsPerHour": 0.06,
  "calculatedRuDollarsPerMonth": 43.68,
  "calculatedEgressPerMonth": 0,
  "calculatedStoragePerMonth": 0.75,
  "calculatedAnalyticalStoragePerMonth": 0.06,
  "calculatedTotalPerMonth": 44.49
}
*/