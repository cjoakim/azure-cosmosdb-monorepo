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
    public class SpecMatrix22Test
    {
        [Fact]
        public void TestSpecMatrix22Test()
        {
            Container c = new Container();
            c.name                  = "container22";
            c.provisioningType      = "autoscale";
            c.replicationType       = "multi-region";
            c.availabilityZone      = false;
            c.regionCount           = 3;
            c.sizeInGB              = 3;
            c.replicatedGBPerMonth  = 0.3;
            c.ruPerSecond           = 400;
            c.synapseLinkEnabled    = true;
            c.maxHistoricalManualRu = 0;
            c.maxHistoricalAutoRu   = 0;

            int    expectedCalculatedMinRU             = 400;
            double expectedCalculatedRatePer100RU      = 0.012;
            double expectedCalculatedRUInHundreds      = 4;
            double expectedCalculatedRuDollarsPerHour  = 0.048;
            double expectedCalculatedRuDollarsPerMonth = 34.944;
            double expectedCalculatedEgressPerMonth    = 0;
            double expectedCalculatedStoragePerMonth   = 2.25;
            double expectedCalculatedAnalyticalStoragePerMonth = 0.06;
            double expectedCalculatedTotalPerMonth     = 37.254000000000005;

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

container:               container22
provisioning_type:       autoscale
replication_type:        multi-region
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
  "name": "container22",
  "sizeInGB": 3,
  "provisioningType": "autoscale",
  "availabilityZone": false,
  "synapseLinkEnabled": true,
  "replicationType": "multi-region",
  "regionCount": 3,
  "ruPerSecond": 400,
  "maxHistoricalManualRu": 0,
  "maxHistoricalAutoRu": 0,
  "replicatedGBPerMonth": 0.3,
  "calculatedMinRU": 400,
  "calculatedRatePer100RU": 0.012,
  "calculatedRUInHundreds": 4,
  "calculatedRuDollarsPerHour": 0.048,
  "calculatedRuDollarsPerMonth": 34.944,
  "calculatedEgressPerMonth": 0,
  "calculatedStoragePerMonth": 2.25,
  "calculatedAnalyticalStoragePerMonth": 0.06,
  "calculatedTotalPerMonth": 37.254000000000005
}
*/