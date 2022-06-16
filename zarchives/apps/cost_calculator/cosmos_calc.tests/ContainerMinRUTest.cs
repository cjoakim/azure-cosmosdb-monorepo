using System;
using Xunit;

using CJoakim.CosmosCalc;

// Xunit unit tests for class Container.
// Chris Joakim, Microsoft, 2020/10/31

namespace cosmos_calc.tests
{
    public class ContainerMinRUTest
    {
        [Fact]
        public void TestConstructorState()
        {
            Container c = new Container();
            Assert.True(c.sizeInGB == 0.0);
            Assert.True(c.calculatedMinRU == -1);
            Assert.True(c.ruPerSecond == 0.0);
            Assert.True(c.maxHistoricalManualRu == 0.0);
            Assert.True(c.maxHistoricalAutoRu == 0.0);
        }

        [Theory]
        [InlineData(0, 0)]
        [InlineData(401, 500)]
        [InlineData(449, 500)]
        [InlineData(451, 500)]
        [InlineData(499, 500)]
        [InlineData(500, 500)]
        [InlineData(10240, 10300)]
        [InlineData(110001, 110100)]
        [InlineData(110099, 110100)]
        public void TestRoundUpToHundreds(int value, int expected)
        {
            Container c = new Container();
            Assert.True(c.RoundUpToHundreds(value) == expected);
        }

        [Fact]
        public void TestMinValue()
        {
            Container c = new Container();
            int ru = c.CalculateMinRU();
            Assert.True(ru == 400);
        }

        [Theory]
        [InlineData(0.0, 400)]
        [InlineData(10.0, 400)]
        [InlineData(40.0, 400)]
        [InlineData(41.0, 500)]
        [InlineData(49.9, 500)]
        [InlineData(400.0, 4000)]
        [InlineData(401.0, 4100)]
        [InlineData(409.9, 4100)]
        [InlineData(8000.0, 80000)]
        [InlineData(8001.0, 80100)]
        [InlineData(8009.9, 80100)]

        public void TestStorageOnlyMinRU(double gb, int expectedRU)
        {
            Container c = new Container();
            c.sizeInGB = gb;
            int calculatedRU = c.CalculateMinRU();
            Assert.True(calculatedRU == expectedRU);
        }

        [Theory]
        [InlineData(0.0, 0, 0, 400)]
        [InlineData(10.0, 0, 0, 400)]
        [InlineData(10.0, 4000, 0, 400)]
        [InlineData(10.0, 40000, 0, 400)]
        [InlineData(10.0, 41000, 0, 500)]
        [InlineData(10.0, 100000, 0, 1000)]
        [InlineData(10.0, 100100, 0, 1100)]
        [InlineData(10.0, 0, 3900, 400)]
        [InlineData(10.0, 0, 4100, 500)]
        [InlineData(10.0, 0, 100000, 10000)]
        [InlineData(10.0, 0, 100100, 10100)]
        public void TestCalculateMinRU(double gb, int maxManual, int maxAuto, int expectedRU)
        {
            Container c = new Container();
            c.sizeInGB = gb;
            c.maxHistoricalManualRu = maxManual;
            c.maxHistoricalAutoRu = maxAuto;
            int calculatedRU = c.CalculateMinRU();
            Assert.True(calculatedRU == expectedRU);
        }
    }
}
