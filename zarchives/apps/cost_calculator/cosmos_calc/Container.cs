using System;
using System.Collections.Generic;

// Class Container represents a Container in CosmosDB for the purpose
// of calculating costs.
//
// Chris Joakim, Microsoft, 2020/10/31

namespace CJoakim.CosmosCalc
{
    public class Container
    {
        // Instance variables:
        public  string name     { get; set; }
        public  double sizeInGB { get; set; }
        public  string provisioningType { get; set; }
        public  bool   availabilityZone { get; set; }
        public  bool   synapseLinkEnabled { get; set; }
        public  string replicationType  { get; set; }
        public  int    regionCount      { get; set; }
        public  int    ruPerSecond      { get; set; }
        public  int    maxHistoricalManualRu { get; set; }
        public  int    maxHistoricalAutoRu   { get; set; }
        public  double replicatedGBPerMonth { get; set; }
        
        // The above fields are set per the input text file,
        // while the following fields are calculated.

        public  int    calculatedMinRU             { get; set; }
        public  double calculatedRatePer100RU      { get; set; }
        public  double calculatedRUInHundreds      { get; set; }
        public  double calculatedRuDollarsPerHour  { get; set; }
        public  double calculatedRuDollarsPerMonth { get; set; }
        public  double calculatedEgressPerMonth    { get; set; }
        public  double calculatedStoragePerMonth   { get; set; }
        public  double calculatedAnalyticalStoragePerMonth { get; set; }
        public  double calculatedTotalPerMonth     { get; set; }

        public Container()
        {
            this.name = null;
            this.sizeInGB = 0.0;
            this.provisioningType = Constants.PROVISIONING_TYPE_STANDARD;
            this.availabilityZone = false;
            this.replicationType  = Constants.REPLICATION_TYPE_SINGLE_REGION;
            this.regionCount      = 1;
            this.ruPerSecond      = 0;
            this.calculatedMinRU  = -1;
            this.calculatedRatePer100RU = 0;
            this.replicatedGBPerMonth = 0.0;
        }

        public void SetProvisioningType(string type)
        {
            switch (type) {             
                case "standard": 
                    this.provisioningType = Constants.PROVISIONING_TYPE_STANDARD;
                    break; 
                case "autoscale": 
                    this.provisioningType = Constants.PROVISIONING_TYPE_AUTOSCALE;
                    break; 
                case "serverless": 
                    Console.WriteLine("ProvisioningType 'serverless' is not yet supported"); 
                    break; 
                default: 
                    Console.WriteLine("Unknown value in SetProvisioningType: " + type); 
                    break; 
            }
        }

        public void SetReplicationType(string type)
        {
            switch (type) {             
                case "single": 
                    this.replicationType = Constants.REPLICATION_TYPE_SINGLE_REGION;
                    break; 
                case "multi-region": 
                    this.replicationType = Constants.REPLICATION_TYPE_MULTI_REGION;
                    break; 
                case "multi-master": 
                    this.replicationType = Constants.REPLICATION_TYPE_MULTI_MASTER;
                    break; 
                default: 
                    Console.WriteLine("Unknown value in SetReplicationType: " + type); 
                    break; 
            }
        }

        public void SetSizeInBytes(double n)
        {
            this.sizeInGB = n / Math.Pow(1024, 3);
        }

        public void SetSizeInMB(double n)
        {
            this.sizeInGB = n / 1024.0;
        }

        public void SetSizeInTB(double n)
        {
            this.sizeInGB = n * 1024.0;
        }

        public void SetSizeInPB(double n)
        {
            this.sizeInGB = n * 1024.0 * 1024.0;
        }

        public int CalculateMinRU()
        {
            int min1 = Constants.ABSOLUTE_MIN_THROUGHPUT;
            int min2 = MinRuBasedOnGB();
            int min3 = MinRuBasedOnManualProvisioning();
            int min4 = MinRuBasedOnAutoProvisioning();

            List<int> minimums = new List<int>() {min1, min2, min3, min4};
            minimums.Sort();
            calculatedMinRU = RoundUpToHundreds(minimums[minimums.Count - 1]);
            return calculatedMinRU;
        }

        public int RoundUpToHundreds(int ru) 
        {
            double fraction = ((double) ru) / 100.0;
            return (int) Math.Round(fraction, 0, MidpointRounding.ToPositiveInfinity) * 100;
        }

        private int MinRuBasedOnGB()
        {
            return (int) sizeInGB * 10;
        }

        private int MinRuBasedOnManualProvisioning()
        {
            if (maxHistoricalManualRu > 0)
            {
                return (int) (maxHistoricalManualRu / 100);
            }
            else
            {
                return 0;
            }
        }

        private int MinRuBasedOnAutoProvisioning()
        {
            if (maxHistoricalAutoRu > 0)
            {
                return (int)(maxHistoricalAutoRu / 10);
            }
            else
            {
                return 0;
            }
        }

        public double CalculateCosts()
        {
            CalculateMinRU();
            CalculateHourlyRatePer100RU();
            CalculateEgress();

            calculatedRUInHundreds = ruPerSecond / 100.0;

            calculatedRuDollarsPerHour =
                calculatedRUInHundreds * calculatedRatePer100RU;

            calculatedRuDollarsPerMonth = 
                calculatedRuDollarsPerHour * Constants.HOURS_PER_MONTH;

            calculatedStoragePerMonth = (sizeInGB * Constants.STORAGE_COSTS_PER_GB_PER_MONTH) * ((double) regionCount);

            if (synapseLinkEnabled)
            {
                calculatedAnalyticalStoragePerMonth = (sizeInGB * Constants.ANALYTICAL_STORAGE_COSTS_PER_GB_PER_MONTH);
            }

            calculatedTotalPerMonth =
                calculatedRuDollarsPerMonth +
                calculatedStoragePerMonth +
                calculatedEgressPerMonth +
                calculatedAnalyticalStoragePerMonth;

            return calculatedTotalPerMonth;
        }

        public double CalculateHourlyRatePer100RU() 
        {
            calculatedRatePer100RU = Constants.HOURLY_RATE_PER_100_RU_STANDARD_SINGLE_REGION;

            if (provisioningType == Constants.PROVISIONING_TYPE_AUTOSCALE)
            {
                if (replicationType == Constants.REPLICATION_TYPE_SINGLE_REGION)
                {
                    calculatedRatePer100RU = Constants.HOURLY_RATE_PER_100_RU_AUTOSCALE_SINGLE_REGION;
                    if (availabilityZone)
                    {
                        calculatedRatePer100RU =
                            (double) calculatedRatePer100RU * Constants.AVAILABILITY_ZONE_MULTIPLIER;
                    }
                }

                if (replicationType == Constants.REPLICATION_TYPE_MULTI_REGION)
                {
                    calculatedRatePer100RU = Constants.HOURLY_RATE_PER_100_RU_AUTOSCALE_MULTI_REGION;
                }

                if (replicationType == Constants.REPLICATION_TYPE_MULTI_MASTER)
                {
                    calculatedRatePer100RU = Constants.HOURLY_RATE_PER_100_RU_AUTOSCALE_MULTI_MASTER;
                }
            }

            if (provisioningType == Constants.PROVISIONING_TYPE_STANDARD)
            {
                if (replicationType == Constants.REPLICATION_TYPE_SINGLE_REGION)
                {
                    calculatedRatePer100RU = Constants.HOURLY_RATE_PER_100_RU_STANDARD_SINGLE_REGION;
                    if (availabilityZone)
                    {
                        calculatedRatePer100RU =
                            calculatedRatePer100RU * Constants.AVAILABILITY_ZONE_MULTIPLIER;
                    }
                }

                if (replicationType == Constants.REPLICATION_TYPE_MULTI_REGION)
                {
                    calculatedRatePer100RU = Constants.HOURLY_RATE_PER_100_RU_STANDARD_MULTI_REGION;
                }

                if (replicationType == Constants.REPLICATION_TYPE_MULTI_MASTER)
                {
                    calculatedRatePer100RU = Constants.HOURLY_RATE_PER_100_RU_STANDARD_MULTI_MASTER;
                }
            }

            if (provisioningType == Constants.PROVISIONING_TYPE_SERVERLESS)
            {
                throw new Exception("provisioningType " + Constants.PROVISIONING_TYPE_SERVERLESS + " is not yet supported by this calculator");
            }

            return calculatedRatePer100RU;
        }

        public double CalculateEgress()
        {
            calculatedEgressPerMonth = 0.0;

            if (regionCount > 1)
            {
                if (replicatedGBPerMonth > Constants.EGRESS_TIER_1_MIN_GB)
                {
                    double tier1GB = GBInEgressTier(Constants.EGRESS_TIER_1_MIN_GB, Constants.EGRESS_TIER_1_MAX_GB);
                    double tier2GB = GBInEgressTier(Constants.EGRESS_TIER_2_MIN_GB, Constants.EGRESS_TIER_2_MAX_GB);
                    double tier3GB = GBInEgressTier(Constants.EGRESS_TIER_3_MIN_GB, Constants.EGRESS_TIER_3_MAX_GB);
                    double tier4GB = GBInEgressTier(Constants.EGRESS_TIER_4_MIN_GB, Constants.EGRESS_TIER_4_MAX_GB);

                    //Console.WriteLine("tier1GB: " + tier1GB);
                    //Console.WriteLine("tier2GB: " + tier2GB);
                    //Console.WriteLine("tier3GB: " + tier3GB);
                    //Console.WriteLine("tier4GB: " + tier4GB);

                    calculatedEgressPerMonth =
                        tier1GB * Constants.EGRESS_TIER_1_RATE +
                        tier2GB * Constants.EGRESS_TIER_2_RATE +
                        tier3GB * Constants.EGRESS_TIER_3_RATE +
                        tier4GB * Constants.EGRESS_TIER_4_RATE;
                }
            }
            return calculatedEgressPerMonth * ((double) regionCount - 1);
        }

        private double GBInEgressTier(double tierMin, double tierMax)
        {
            double gb = 0;
            double tierRange = tierMax - tierMin;

            if (replicatedGBPerMonth > tierMin)
            {
                gb = replicatedGBPerMonth - tierMin;
                if (gb > tierRange)
                {
                    gb = tierRange;
                }
            }
            return gb;
        }
    }
}
