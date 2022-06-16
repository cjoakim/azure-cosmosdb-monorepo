using System;
using Xunit;

using CJoakim.CosmosCalc;

// Xunit unit tests for class Container.
// Chris Joakim, Microsoft, 2020/10/31

namespace cosmos_calc.tests
{
    public class ContainerTypeTest
    {
        [Fact]
        public void TestProvisioningType()
        {
            Container c = new Container();
            Assert.True(c.provisioningType == "standard");
            Assert.True(c.replicationType == "single");

            c.SetProvisioningType("autoscale");
            Assert.True(c.provisioningType == "autoscale");

            c.SetProvisioningType("serverless");
            Assert.True(c.provisioningType == "autoscale");

            c.SetProvisioningType("standard");
            Assert.True(c.provisioningType == "standard");

            c.SetProvisioningType(null);
            Assert.True(c.provisioningType == "standard");

            c.SetProvisioningType("oops");
            Assert.True(c.provisioningType == "standard");
            Assert.True(c.replicationType == "single");
        }

        [Fact]
        public void TestReplicationType()
        {
            Container c = new Container();
            Assert.True(c.replicationType == "single");
            Assert.True(c.provisioningType == "standard");

            c.SetReplicationType("multi-region");
            Assert.True(c.replicationType == "multi-region");

            c.SetReplicationType("multi-master");
            Assert.True(c.replicationType == "multi-master");

            c.SetReplicationType(null);
            Assert.True(c.replicationType == "multi-master");

            c.SetReplicationType("oops");
            Assert.True(c.replicationType == "multi-master");

            Assert.True(c.provisioningType == "standard");

            c.SetReplicationType("single");
            Assert.True(c.replicationType == "single");
        }
    }
}
