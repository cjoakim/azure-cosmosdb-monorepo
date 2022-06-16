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
    public class SpecMatrix21Test
    {
        [Fact]
        public void TestSpecMatrix21Test()
        {
            Container c = new Container();
            c.name                  = "container21";
            c.provisioningType      = "autoscale";
            c.replicationType       = "single";
            c.availabilityZone      = false;
            c.regionCount           = 1;
            c.sizeInGB              = 30000;
            c.replicatedGBPerMonth  = 0.0;
            c.ruPerSecond           = 300000;
            c.synapseLinkEnabled    = true;
            c.maxHistoricalManualRu = 0;
            c.maxHistoricalAutoRu   = 0;

            int    expectedCalculatedMinRU             = 300000;
            double expectedCalculatedRatePer100RU      = 0.012;
            double expectedCalculatedRUInHundreds      = 3000;
            double expectedCalculatedRuDollarsPerHour  = 36;
            double expectedCalculatedRuDollarsPerMonth = 26208;
            double expectedCalculatedEgressPerMonth    = 0;
            double expectedCalculatedStoragePerMonth   = 7500;
            double expectedCalculatedAnalyticalStoragePerMonth = 600;
            double expectedCalculatedTotalPerMonth     = 34308;

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

container:               container21
provisioning_type:       autoscale
replication_type:        single
region_count:            1
availability_zone:       false
size_in_gb:              30000
replicated_gb_per_month: 0.0
ru_per_second:           300000
synapse_link_enabled:    true
calculate_costs:         true

*/

/*
{
  "name": "container21",
  "sizeInGB": 30000,
  "provisioningType": "autoscale",
  "availabilityZone": false,
  "synapseLinkEnabled": true,
  "replicationType": "single",
  "regionCount": 1,
  "ruPerSecond": 300000,
  "maxHistoricalManualRu": 0,
  "maxHistoricalAutoRu": 0,
  "replicatedGBPerMonth": 0,
  "calculatedMinRU": 300000,
  "calculatedRatePer100RU": 0.012,
  "calculatedRUInHundreds": 3000,
  "calculatedRuDollarsPerHour": 36,
  "calculatedRuDollarsPerMonth": 26208,
  "calculatedEgressPerMonth": 0,
  "calculatedStoragePerMonth": 7500,
  "calculatedAnalyticalStoragePerMonth": 600,
  "calculatedTotalPerMonth": 34308
}
*/