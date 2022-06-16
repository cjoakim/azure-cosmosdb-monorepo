using System;
using Xunit;

using CJoakim.CosmosCalc;

// Xunit unit tests for class Container.
// Chris Joakim, Microsoft, 2020/10/31

// dotnet test --filter "FullyQualifiedName=cosmos_calc.tests.ContainerEgressTest.TestEgress"

namespace cosmos_calc.tests
{
    public class ContainerEgressTest
    {
        [Theory]
        [InlineData(0.0, 1, 0.0)]
        [InlineData(6.0, 2, 0.087)]
        [InlineData(12.0, 2, 0.601)]
        [InlineData(52.0, 2, 3.8950000000000005)]
        [InlineData(152.0, 3, 21.71)]
        public void TestEgress(
            double   egressGB,
            int      regionCount,
            double   expectedCost)
        {
            Container c = new Container();
            c.replicatedGBPerMonth = egressGB;
            c.regionCount = regionCount;
            double calculatedCost = c.CalculateEgress();
            double tolerance = 0.000001;

            Console.WriteLine("egressGB: {0}, regionCount: {1}, cost: {2}", egressGB, regionCount, calculatedCost);
            Assert.True(calculatedCost + tolerance > expectedCost);
            Assert.True(calculatedCost - tolerance < expectedCost);

            // Egress 152 GB example
            //calculatedCost =
            //    (5.0 * Constants.EGRESS_TIER_1_RATE) +
            //    (40.0 * Constants.EGRESS_TIER_2_RATE) +
            //    (100.0 * Constants.EGRESS_TIER_3_RATE) +
            //    (2.0 * Constants.EGRESS_TIER_4_RATE);
            //Console.WriteLine("Egress 152 GB example: " + calculatedCost);
        }
    }
}
