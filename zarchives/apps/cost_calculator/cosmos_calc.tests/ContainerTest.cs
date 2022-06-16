using System;
using Xunit;

using CJoakim.CosmosCalc;

// Xunit unit tests for class Container.
// Chris Joakim, Microsoft, 2020/10/31

namespace cosmos_calc.tests
{
    public class ContainerTest
    {
        [Fact]
        public void ConstructorTest()
        {
            Container c = new Container();
            Assert.True(c.name == null);
            Assert.True(c.sizeInGB == 0.0);
            Assert.True(c.calculatedMinRU == -1);
            Assert.True(c.availabilityZone == false);
            Assert.True(c.provisioningType == "standard");
            Assert.True(c.replicationType == "single");
            Assert.True(c.regionCount == 1);
            Assert.True(c.ruPerSecond == 0.0);

            Assert.True(c.calculatedRatePer100RU == 0);
            Assert.True(c.calculatedTotalPerMonth == 0.0);
        }
    }
}
