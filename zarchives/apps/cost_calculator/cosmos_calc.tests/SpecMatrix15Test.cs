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
    public class SpecMatrix15Test
    {
        [Fact]
        public void TestSpecMatrix15Test()
        {
            Container c = new Container();
            c.name                  = "container15";
            c.provisioningType      = "standard";
            c.replicationType       = "multi-master";
            c.availabilityZone      = false;
            c.regionCount           = 3;
            c.sizeInGB              = 30000;
            c.replicatedGBPerMonth  = 3000.0;
            c.ruPerSecond           = 300000;
            c.synapseLinkEnabled    = true;
            c.maxHistoricalManualRu = 0;
            c.maxHistoricalAutoRu   = 0;

            int    expectedCalculatedMinRU             = 300000;
            double expectedCalculatedRatePer100RU      = 0.016;
            double expectedCalculatedRUInHundreds      = 3000;
            double expectedCalculatedRuDollarsPerHour  = 48;
            double expectedCalculatedRuDollarsPerMonth = 34944;
            double expectedCalculatedEgressPerMonth    = 153.255;
            double expectedCalculatedStoragePerMonth   = 22500;
            double expectedCalculatedAnalyticalStoragePerMonth = 600;
            double expectedCalculatedTotalPerMonth     = 58197.255;

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

container:               container15
provisioning_type:       standard
replication_type:        multi-master
region_count:            3
availability_zone:       false
size_in_gb:              30000
replicated_gb_per_month: 3000.0
ru_per_second:           300000
synapse_link_enabled:    true
calculate_costs:         true

*/

/*
{
  "name": "container15",
  "sizeInGB": 30000,
  "provisioningType": "standard",
  "availabilityZone": false,
  "synapseLinkEnabled": true,
  "replicationType": "multi-master",
  "regionCount": 3,
  "ruPerSecond": 300000,
  "maxHistoricalManualRu": 0,
  "maxHistoricalAutoRu": 0,
  "replicatedGBPerMonth": 3000,
  "calculatedMinRU": 300000,
  "calculatedRatePer100RU": 0.016,
  "calculatedRUInHundreds": 3000,
  "calculatedRuDollarsPerHour": 48,
  "calculatedRuDollarsPerMonth": 34944,
  "calculatedEgressPerMonth": 153.255,
  "calculatedStoragePerMonth": 22500,
  "calculatedAnalyticalStoragePerMonth": 600,
  "calculatedTotalPerMonth": 58197.255
}
*/