using System;

using System.Collections.Generic;
using System.IO;
using System.Text.Json;
using Xunit;

using CJoakim.CosmosCalc;

// Xunit unit tests for class SpecProcessor.
// Chris Joakim, Microsoft, 2020/10/31

// dotnet test --filter "FullyQualifiedName=cosmos_calc.tests.SpecProcessorTest.Spec3MB_Autoscale_InMB_Test"


namespace cosmos_calc.tests
{
    public class SpecProcessorTest
    {
        [Fact]
        public void Spec0_Invalid_Test()
        {
            List<string> specLines = arrayToList(Spec0_Invalid().Split("\n"));
            SpecProcessor sp = new SpecProcessor(specLines);
            sp.process();

            Assert.True(sp.currentContainer == null);
        }

        private string Spec0_Invalid()
        {
            return @"
what_goes_here: I'm not sure
recommendation: Read the README.md documentation
";
        }

        [Fact]
        public void Spec1Test()
        {
            List<string> specLines = arrayToList(Spec1().Split("\n"));
            SpecProcessor sp = new SpecProcessor(specLines);
            sp.process();

            Assert.True(sp.calculationResults.Count == 1);
            string json = sp.calculationResults[0];
            Container c = JsonSerializer.Deserialize<Container>(json);

            // displayObjectAsJson(c);

            Assert.True(c.name == "events1");
            Assert.True(c.provisioningType == "standard");
            Assert.True(c.replicationType == "single");
            Assert.True(c.availabilityZone == false);

            Assert.True(c.sizeInGB == 1.0);

            Assert.True(c.regionCount == 1);
            Assert.True(c.ruPerSecond == 500);
            Assert.True(c.maxHistoricalManualRu == 1000);
            Assert.True(c.maxHistoricalAutoRu == 0);

            Assert.True(c.calculatedMinRU == 400);
            Assert.True(c.calculatedRatePer100RU == 0.008);
            Assert.True(c.calculatedRUInHundreds == 5);
            Assert.True(c.calculatedRuDollarsPerHour == 0.04);

            Assert.True(c.calculatedRuDollarsPerMonth == 29.12);
            Assert.True(c.calculatedStoragePerMonth == 0.25);
            Assert.True(c.calculatedEgressPerMonth == 0.0);
            Assert.True(c.calculatedAnalyticalStoragePerMonth == 0.0);
            Assert.True(c.calculatedTotalPerMonth == 29.37);
        }

        private string Spec1()
        {
            return @"
container:                   events1
provisioning_type:          standard
replication_type:             single
region_count:                      1
size_in_gb:                        1
max_historical_manual_ru:       1000
max_historical_auto_ru:            0
ru_per_second:                   500
availability_zone:             false
synapse_link_enabled:          false
calculate_costs:                true
";
        }

        [Fact]
        public void Spec2_WithAvailabilityZoneTest()
        {
            List<string> specLines = arrayToList(Spec2_WithAvailabilityZone().Split("\n"));
            SpecProcessor sp = new SpecProcessor(specLines);
            sp.process();

            Assert.True(sp.calculationResults.Count == 1);
            string json = sp.calculationResults[0];
            Container c = JsonSerializer.Deserialize<Container>(json);

            // displayObjectAsJson(c);

            Assert.True(c.name == "events2");
            Assert.True(c.provisioningType == "standard");
            Assert.True(c.replicationType == "single");
            Assert.True(c.availabilityZone == true);

            Assert.True(c.sizeInGB == 1.0);

            Assert.True(c.regionCount == 1);
            Assert.True(c.ruPerSecond == 500);
            Assert.True(c.maxHistoricalManualRu == 1000);
            Assert.True(c.maxHistoricalAutoRu == 0);

            Assert.True(c.calculatedMinRU == 400);
            Assert.True(c.calculatedRatePer100RU == 0.010);
            Assert.True(c.calculatedRUInHundreds == 5);
            Assert.True(c.calculatedRuDollarsPerHour == 0.05);

            Assert.True(c.calculatedRuDollarsPerMonth == 36.4);
            Assert.True(c.calculatedStoragePerMonth == 0.25);
            Assert.True(c.calculatedTotalPerMonth == 36.65);
        }

        private string Spec2_WithAvailabilityZone()
        {
            return @"
container:                   events2
provisioning_type:          standard
replication_type:             single
region_count:                      1
size_in_gb:                        1
max_historical_manual_ru:       1000
max_historical_auto_ru:            0
ru_per_second:                   500
availability_zone:              true
calculate_costs:                true
";
        }

        [Fact]
        public void Spec3B_Autoscale_InBytes_Test()
        {
            List<string> specLines = arrayToList(Spec3_Autoscale_InBytes().Split("\n"));
            SpecProcessor sp = new SpecProcessor(specLines);
            sp.process();

            Assert.True(sp.calculationResults.Count == 1);
            string json = sp.calculationResults[0];
            Container c = JsonSerializer.Deserialize<Container>(json);

            //displayObjectAsJson(c);

            Assert.True(c.name == "spec3b");
            Assert.True(c.provisioningType == "autoscale");
            Assert.True(c.replicationType == "multi-master");
            Assert.True(c.availabilityZone == false);

            Assert.True(c.sizeInGB == 15.0);

            Assert.True(c.regionCount == 2);
            Assert.True(c.ruPerSecond == 20000);
            Assert.True(c.maxHistoricalManualRu == 0);
            Assert.True(c.maxHistoricalAutoRu == 0);

            Assert.True(c.calculatedMinRU == 400);
            Assert.True(c.calculatedRatePer100RU == 0.016);
            Assert.True(c.calculatedRUInHundreds == 200);
            Assert.True(c.calculatedRuDollarsPerHour == 3.2);

            Assert.True(c.calculatedRuDollarsPerMonth == 2329.6);
            Assert.True(c.calculatedStoragePerMonth == 7.5);
            Assert.True(c.calculatedEgressPerMonth == 0.0);
            Assert.True(c.calculatedTotalPerMonth == 2337.1);
        }

        private string Spec3_Autoscale_InBytes()
        {
            return @"
container:                    spec3b
provisioning_type:         autoscale
replication_type:       multi-master
region_count:                      2
size_in_bytes:           16106127360
ru_per_second:                 20000
replicated_gb_per_month:         4.9
calculate_costs:                true
";
        }

        [Fact]
        public void Spec3MB_Autoscale_InMB_Test()
        {
            List<string> specLines = arrayToList(Spec3_Autoscale_InMB().Split("\n"));
            SpecProcessor sp = new SpecProcessor(specLines);
            sp.process();

            Assert.True(sp.calculationResults.Count == 1);
            string json = sp.calculationResults[0];
            Container c = JsonSerializer.Deserialize<Container>(json);

            //displayObjectAsJson(c);

            // Same values as Spec3_Autoscale_InBytes_Test
            Assert.True(c.sizeInGB == 15.0);
            Assert.True(c.calculatedRuDollarsPerMonth == 2329.6);
            Assert.True(c.calculatedStoragePerMonth == 7.5);
            Assert.True(c.calculatedEgressPerMonth == 0.087);
            Assert.True(c.calculatedAnalyticalStoragePerMonth == 0.3);
            Assert.True(c.calculatedTotalPerMonth == 2337.487);
        }

        private string Spec3_Autoscale_InMB()
        {
            return @"
container:                   spec3mb
provisioning_type:         autoscale
replication_type:       multi-master
region_count:                      2
size_in_mb:                    15360
ru_per_second:                 20000
replicated_gb_per_month:           6
synapse_link_enabled:           true
calculate_costs:                true
";
        }

        [Fact]
        public void Spec4_Autoscale_InTB_Test()
        {
            List<string> specLines = arrayToList(Spec4_Autoscale_InTB().Split("\n"));
            SpecProcessor sp = new SpecProcessor(specLines);
            sp.process();

            Assert.True(sp.calculationResults.Count == 1);
            string json = sp.calculationResults[0];
            Container c = JsonSerializer.Deserialize<Container>(json);

            //displayObjectAsJson(c);

            Assert.True(c.name == "spec4");
            Assert.True(c.sizeInGB == 6348.8);
            Assert.True(c.calculatedMinRU == 63500);
            Assert.True(c.calculatedStoragePerMonth == 3174.4);
        }

        private string Spec4_Autoscale_InTB()
        {
            return @"
container:                     spec4
provisioning_type:         autoscale
replication_type:       multi-master
region_count:                      2
size_in_tb:                      6.2
ru_per_second:                 20000
calculate_costs:                true
";
        }

        [Fact]
        public void Spec5_Autoscale_InPB_Test()
        {
            List<string> specLines = arrayToList(Spec5_Autoscale_InPB().Split("\n"));
            SpecProcessor sp = new SpecProcessor(specLines);
            sp.process();

            Assert.True(sp.calculationResults.Count == 1);
            string json = sp.calculationResults[0];
            Container c = JsonSerializer.Deserialize<Container>(json);

            //displayObjectAsJson(c);

            Assert.True(c.name == "spec5");
            Assert.True(c.sizeInGB == 67108864);
            Assert.True(c.calculatedMinRU == 671088700);
            Assert.True(c.calculatedStoragePerMonth == 33554432);
        }

        private string Spec5_Autoscale_InPB()
        {
            return @"
container:                     spec5
provisioning_type:         autoscale
replication_type:       multi-master
region_count:                      2
size_in_pb:                       64
ru_per_second:                100000
calculate_costs:                true
";
        }

        private List<string> arrayToList(string[] lines)
        {
            List<string> specLines = new List<string>();
            foreach (string line in lines)
            {
                specLines.Add(line);
            }
            return specLines;
        }

        private void displayObjectAsJson(object obj)
        {
            var options = new JsonSerializerOptions
            {
                WriteIndented = true,
            };
            string result = JsonSerializer.Serialize(obj, options);
            Console.WriteLine(result);
        }
    }
}
