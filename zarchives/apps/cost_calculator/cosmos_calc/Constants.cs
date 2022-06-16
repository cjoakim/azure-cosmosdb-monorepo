// Abstract class used to define hard-coded cost and calculation constants.
// Chris Joakim, Microsoft, 2020/10/31

namespace CJoakim.CosmosCalc
{
    public class Constants
    {
        public const string PROVISIONING_TYPE_STANDARD   = "standard";
        public const string PROVISIONING_TYPE_AUTOSCALE  = "autoscale";
        public const string PROVISIONING_TYPE_SERVERLESS = "serverless";

        public const string REPLICATION_TYPE_SINGLE_REGION = "single";
        public const string REPLICATION_TYPE_MULTI_REGION  = "multi-region";
        public const string REPLICATION_TYPE_MULTI_MASTER  = "multi-master";

        public const int    ABSOLUTE_MIN_THROUGHPUT = 400;
        public const double AVAILABILITY_ZONE_MULTIPLIER = 1.25;

        public const double HOURLY_RATE_PER_100_RU_STANDARD_SINGLE_REGION  = 0.008;
        public const double HOURLY_RATE_PER_100_RU_STANDARD_MULTI_REGION   = 0.012;
        public const double HOURLY_RATE_PER_100_RU_STANDARD_MULTI_MASTER   = 0.016;

        public const double HOURLY_RATE_PER_100_RU_AUTOSCALE_SINGLE_REGION = 0.012;
        public const double HOURLY_RATE_PER_100_RU_AUTOSCALE_MULTI_REGION  = 0.012;
        public const double HOURLY_RATE_PER_100_RU_AUTOSCALE_MULTI_MASTER  = 0.016;

        public const double STORAGE_COSTS_PER_GB_PER_MONTH = 0.25;
        public const double ANALYTICAL_STORAGE_COSTS_PER_GB_PER_MONTH = 0.02;

        // EGRESS - see https://azure.microsoft.com/en-us/pricing/details/bandwidth/

        public const double EGRESS_TIER_1_MIN_GB = 5.0;
        public const double EGRESS_TIER_1_MAX_GB = 10.0;
        public const double EGRESS_TIER_1_RATE = 0.087;

        public const double EGRESS_TIER_2_MIN_GB = 10.0;
        public const double EGRESS_TIER_2_MAX_GB = 50.0;
        public const double EGRESS_TIER_2_RATE = 0.083;

        public const double EGRESS_TIER_3_MIN_GB = 50.0;
        public const double EGRESS_TIER_3_MAX_GB = 150.0;
        public const double EGRESS_TIER_3_RATE = 0.07;

        public const double EGRESS_TIER_4_MIN_GB = 150.0;
        public const double EGRESS_TIER_4_MAX_GB = 999999999999.0; // Contact Us!
        public const double EGRESS_TIER_4_RATE = 0.05;

        public const double WEEKS_PER_MONTH = 52.0 / 12.0;
        public const double HOURS_PER_WEEK = (24.0 * 7.0);
        public const double HOURS_PER_MONTH = WEEKS_PER_MONTH * HOURS_PER_WEEK;
    }
}
