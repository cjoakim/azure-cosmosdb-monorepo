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
    public class SpecMatrix13Test
    {
        [Fact]
        public void TestSpecMatrix13Test()
        {
            Container c = new Container();
            c.name                  = "container13";
            c.provisioningType      = "standard";
            c.replicationType       = "multi-master";
            c.availabilityZone      = false;
            c.regionCount           = 3;
            c.sizeInGB              = 3;
            c.replicatedGBPerMonth  = 0.3;
            c.ruPerSecond           = 400;
            c.synapseLinkEnabled    = true;
            c.maxHistoricalManualRu = 0;
            c.maxHistoricalAutoRu   = 0;

            int    expectedCalculatedMinRU             = 400;
            double expectedCalculatedRatePer100RU      = 0.016;
            double expectedCalculatedRUInHundreds      = 4;
            double expectedCalculatedRuDollarsPerHour  = 0.064;
            double expectedCalculatedRuDollarsPerMonth = 46.592;
            double expectedCalculatedEgressPerMonth    = 0;
            double expectedCalculatedStoragePerMonth   = 2.25;
            double expectedCalculatedAnalyticalStoragePerMonth = 0.06;
            double expectedCalculatedTotalPerMonth     = 48.902;

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

container:               container13
provisioning_type:       standard
replication_type:        multi-master
region_count:            3
availability_zone:       false
size_in_gb:              3
replicated_gb_per_month: 0.3
ru_per_second:           400
synapse_link_enabled:    true
calculate_costs:         true

*/

/*
{
  "name": "container13",
  "sizeInGB": 3,
  "provisioningType": "standard",
  "availabilityZone": false,
  "synapseLinkEnabled": true,
  "replicationType": "multi-master",
  "regionCount": 3,
  "ruPerSecond": 400,
  "maxHistoricalManualRu": 0,
  "maxHistoricalAutoRu": 0,
  "replicatedGBPerMonth": 0.3,
  "calculatedMinRU": 400,
  "calculatedRatePer100RU": 0.016,
  "calculatedRUInHundreds": 4,
  "calculatedRuDollarsPerHour": 0.064,
  "calculatedRuDollarsPerMonth": 46.592,
  "calculatedEgressPerMonth": 0,
  "calculatedStoragePerMonth": 2.25,
  "calculatedAnalyticalStoragePerMonth": 0.06,
  "calculatedTotalPerMonth": 48.902
}
*/