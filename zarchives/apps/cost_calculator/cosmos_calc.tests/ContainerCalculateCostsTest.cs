using System;
using System.Text;
using System.Text.Json;
using System.Text.Json.Serialization;

using Xunit;

using CJoakim.CosmosCalc;

// Xunit unit tests for class Container.
// Chris Joakim, Microsoft, 2020/10/31

namespace cosmos_calc.tests
{

public class ContainerCalculateCostsTest
    {
        [Theory]
        [InlineData("case1", "standard", "single", 1, false, 5, 400, 24.546, 1.25)]
        [InlineData("case2", "standard", "single", 1, true, 20.0, 1000, 77.8, 5.0 )]
        [InlineData("case3", "standard", "multi-region", 2, false, 1000, 50000, 4868.0, 500.0)]
        [InlineData("case4", "standard", "multi-master", 2, false, 1000, 50000, 6324.0, 500.0)]
        [InlineData("case5", "autoscale", "single", 1, false, 5, 400, 36.194, 1.25)]
        [InlineData("case6", "autoscale", "single", 1, true, 20.0, 1000, 114.2, 5.0 )]
        [InlineData("case7", "autoscale", "multi-region", 2, false, 1000, 50000, 4868.0, 500.0)]
        [InlineData("case8", "autoscale", "multi-master", 2, false, 1000, 50000, 6324.0, 500.0)]
        public void TestCalculateHourlyRatePer100RU(
            string caseName,
            string provType,
            string replType,
            int    regionCount,
            bool   availZone,
            double sizeInGB,
            int    ru,
            double expectedTotalPerMonth,
            double expectedStorageCostsPerMonth)
        {
            Container c = new Container();
            c.name             = caseName;
            c.provisioningType = provType;
            c.replicationType  = replType;
            c.availabilityZone = availZone;
            c.regionCount      = regionCount;
            c.sizeInGB         = sizeInGB;
            c.ruPerSecond      = ru;
            double tolerance   = 0.000001;

            double costs = c.CalculateCosts();
            var options = new JsonSerializerOptions
            {
                WriteIndented = true,
            };

            Console.WriteLine("case: {0}, storage: {1}, total: {2}",
                c.name, c.calculatedStoragePerMonth, c.calculatedTotalPerMonth);

            if (c.name == "case8")
            {
                Console.WriteLine(JsonSerializer.Serialize(c, options));
            }

            Assert.True(c.calculatedStoragePerMonth + tolerance > expectedStorageCostsPerMonth);
            Assert.True(c.calculatedStoragePerMonth - tolerance < expectedStorageCostsPerMonth);

            Assert.True(c.calculatedTotalPerMonth + tolerance > expectedTotalPerMonth);
            Assert.True(c.calculatedTotalPerMonth - tolerance < expectedTotalPerMonth);
        }
    }
}
