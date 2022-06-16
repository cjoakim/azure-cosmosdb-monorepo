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
    public class SpecMatrix8Test
    {
        [Fact]
        public void TestSpecMatrix8Test()
        {
            Container c = new Container();
            c.name                  = "container8";
            c.provisioningType      = "standard";
            c.replicationType       = "multi-region";
            c.availabilityZone      = false;
            c.regionCount           = 3;
            c.sizeInGB              = 300;
            c.replicatedGBPerMonth  = 30.0;
            c.ruPerSecond           = 3000;
            c.synapseLinkEnabled    = true;
            c.maxHistoricalManualRu = 0;
            c.maxHistoricalAutoRu   = 0;

            int    expectedCalculatedMinRU             = 3000;
            double expectedCalculatedRatePer100RU      = 0.012;
            double expectedCalculatedRUInHundreds      = 30;
            double expectedCalculatedRuDollarsPerHour  = 0.36;
            double expectedCalculatedRuDollarsPerMonth = 262.08;
            double expectedCalculatedEgressPerMonth    = 2.095;
            double expectedCalculatedStoragePerMonth   = 225;
            double expectedCalculatedAnalyticalStoragePerMonth = 6;
            double expectedCalculatedTotalPerMonth     = 495.175;

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

container:               container8
provisioning_type:       standard
replication_type:        multi-region
region_count:            3
availability_zone:       false
size_in_gb:              300
replicated_gb_per_month: 30.0
ru_per_second:           3000
synapse_link_enabled:    true
calculate_costs:         true

*/

/*
{
  "name": "container8",
  "sizeInGB": 300,
  "provisioningType": "standard",
  "availabilityZone": false,
  "synapseLinkEnabled": true,
  "replicationType": "multi-region",
  "regionCount": 3,
  "ruPerSecond": 3000,
  "maxHistoricalManualRu": 0,
  "maxHistoricalAutoRu": 0,
  "replicatedGBPerMonth": 30,
  "calculatedMinRU": 3000,
  "calculatedRatePer100RU": 0.012,
  "calculatedRUInHundreds": 30,
  "calculatedRuDollarsPerHour": 0.36,
  "calculatedRuDollarsPerMonth": 262.08,
  "calculatedEgressPerMonth": 2.095,
  "calculatedStoragePerMonth": 225,
  "calculatedAnalyticalStoragePerMonth": 6,
  "calculatedTotalPerMonth": 495.175
}
*/