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
    public class SpecMatrix20Test
    {
        [Fact]
        public void TestSpecMatrix20Test()
        {
            Container c = new Container();
            c.name                  = "container20";
            c.provisioningType      = "autoscale";
            c.replicationType       = "single";
            c.availabilityZone      = false;
            c.regionCount           = 1;
            c.sizeInGB              = 300;
            c.replicatedGBPerMonth  = 0.0;
            c.ruPerSecond           = 3000;
            c.synapseLinkEnabled    = true;
            c.maxHistoricalManualRu = 0;
            c.maxHistoricalAutoRu   = 0;

            int    expectedCalculatedMinRU             = 3000;
            double expectedCalculatedRatePer100RU      = 0.012;
            double expectedCalculatedRUInHundreds      = 30;
            double expectedCalculatedRuDollarsPerHour  = 0.36;
            double expectedCalculatedRuDollarsPerMonth = 262.08;
            double expectedCalculatedEgressPerMonth    = 0;
            double expectedCalculatedStoragePerMonth   = 75;
            double expectedCalculatedAnalyticalStoragePerMonth = 6;
            double expectedCalculatedTotalPerMonth     = 343.08;

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

container:               container20
provisioning_type:       autoscale
replication_type:        single
region_count:            1
availability_zone:       false
size_in_gb:              300
replicated_gb_per_month: 0.0
ru_per_second:           3000
synapse_link_enabled:    true
calculate_costs:         true

*/

/*
{
  "name": "container20",
  "sizeInGB": 300,
  "provisioningType": "autoscale",
  "availabilityZone": false,
  "synapseLinkEnabled": true,
  "replicationType": "single",
  "regionCount": 1,
  "ruPerSecond": 3000,
  "maxHistoricalManualRu": 0,
  "maxHistoricalAutoRu": 0,
  "replicatedGBPerMonth": 0,
  "calculatedMinRU": 3000,
  "calculatedRatePer100RU": 0.012,
  "calculatedRUInHundreds": 30,
  "calculatedRuDollarsPerHour": 0.36,
  "calculatedRuDollarsPerMonth": 262.08,
  "calculatedEgressPerMonth": 0,
  "calculatedStoragePerMonth": 75,
  "calculatedAnalyticalStoragePerMonth": 6,
  "calculatedTotalPerMonth": 343.08
}
*/