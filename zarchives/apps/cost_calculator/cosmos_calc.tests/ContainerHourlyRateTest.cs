using System;
using Xunit;

using CJoakim.CosmosCalc;

// Xunit unit tests for class Container.
// Chris Joakim, Microsoft, 2020/10/31

namespace cosmos_calc.tests
{
    public class ContainerHourlyRateTest
    {
        [Theory]
        [InlineData("standard", "single", 1, false, 0.008)]
        [InlineData("standard", "single", 1, true, 0.010)]
        [InlineData("standard", "multi-region", 2, false, 0.012)]
        [InlineData("standard", "multi-master", 2, false, 0.016)]
        [InlineData("autoscale", "single", 1, false, 0.012)]
        [InlineData("autoscale", "single", 1, true, 0.015)]
        [InlineData("autoscale", "multi-region", 2, false, 0.012)]
        [InlineData("autoscale", "multi-master", 2, false, 0.016)]
        public void TestCalculateHourlyRatePer100RU(
            string provType,
            string replType,
            int    regionCount,
            bool   availZone,
            double expectedRate)
        {
            Container c = new Container();
            c.provisioningType = provType;
            c.replicationType  = replType;
            c.availabilityZone = availZone;
            c.regionCount      = regionCount;
            double calculatedRate = c.CalculateHourlyRatePer100RU();
            double tolerance = 0.000001;

            Console.WriteLine("calc: {0}, expected: {1}", calculatedRate, expectedRate);
            Assert.True(calculatedRate + tolerance > expectedRate);
            Assert.True(calculatedRate - tolerance < expectedRate);
        }

        [Theory]
        [InlineData("serverless", "single")]
        public void TestCalculateHourlyRatePer100RU_Serverless(
            string provType,
            string replType)
        {
            Container c = new Container();
            c.provisioningType = provType;
            c.replicationType = replType;
            try
            {
                double calculatedRate = c.CalculateHourlyRatePer100RU();
                Assert.True(false, "an exception should have been thrown by the impl code");
            }
            catch (Exception e)
            {
                string expected = "provisioningType serverless is not yet supported by this calculator";
                Assert.True(e.Message == expected);
            }
        }
    }
}
