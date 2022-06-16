using System;
using Xunit;

using CJoakim.CosmosCalc;

// Xunit unit tests for class Container.
// Chris Joakim, Microsoft, 2020/10/31

namespace cosmos_calc.tests
{
    public class ContainerSizeTest
    {
        [Fact]
        public void TestInitialSize()
        {
            Container c = new Container();
            Assert.True(c.sizeInGB == 0);
        }

        [Fact]
        public void TestNonZeroSizes()
        {
            Container c = new Container();
            double mbs = 1;
            double gbs = 6.87;
            double tbs = 112.0;
            double pbs = 53.1;
            double b   = 1024.0 * 1024.0 * 1024.0 * 3.14;
            double tolerance = 0.000001;

            c.sizeInGB = gbs;
            Assert.True(c.sizeInGB + tolerance > gbs);
            Assert.True(c.sizeInGB - tolerance < gbs);

            c.SetSizeInMB(mbs);
            Assert.True(c.sizeInGB + tolerance > (mbs / 1024.0));
            Assert.True(c.sizeInGB - tolerance < (mbs / 1024.0));

            c.SetSizeInTB(tbs);
            Assert.True(c.sizeInGB + tolerance > (tbs * 1024.0));
            Assert.True(c.sizeInGB - tolerance < (tbs * 1024.0));

            c.SetSizeInPB(pbs);
            Assert.True(c.sizeInGB + tolerance > (pbs * 1024.0 * 1024.0));
            Assert.True(c.sizeInGB - tolerance < (pbs * 1024.0 * 1024.0));

            c.SetSizeInBytes(b);
            Assert.True(c.sizeInGB + tolerance > (3.14));
            Assert.True(c.sizeInGB - tolerance < (3.14));
        }
    }
}
