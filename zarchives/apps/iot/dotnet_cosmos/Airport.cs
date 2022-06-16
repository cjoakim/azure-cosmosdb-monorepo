using System;
using Newtonsoft.Json;

// Instances of this class represent an Airport in the OpenFlights CSV data, like this:
// AirportId,Name,City,Country,IataCode,IcaoCode,Latitude,Longitude,Altitude,TimezoneNum,Dst,TimezoneCode
// 3682,"Hartsfield Jackson Atlanta Intl","Atlanta","United States","ATL","KATL",33.636719,-84.428067,1026,-5,"A","America/New_York"
//
// Chris Joakim, Microsoft, 2020/10/29

namespace CJoakim.Cosmos
{
    public class Airport
    {
        public string id { get; set; }
        public string pk { get; set; }
        public int    AirportId { get; set; }
        public string Name { get; set; }
        public string City { get; set; }
        public string Country { get; set; }
        public string IataCode { get; set; }
        public string IcaoCode { get; set; }
        public double Latitude { get; set; }
        public double Longitude { get; set; }
        public Location location { get; set; }
        public double Altitude { get; set; }
        public float  TimezoneNum { get; set; }
        public string Dst { get; set; }
        public string TimezoneCode { get; set; }
        public long   Epoch { get; set; }

        public Airport()
        {
            // Default constructor
        }

        public void postParse()
        {
            this.pk = IataCode;
            this.location = new Location(this.Latitude, this.Longitude);
            if (this.id == null)
            {
                this.id = Guid.NewGuid().ToString();
            }
            this.Epoch = new DateTimeOffset(DateTime.UtcNow).ToUnixTimeMilliseconds();


        }

        public void UpdateEpoch()
        {
            this.Epoch = new DateTimeOffset(DateTime.UtcNow).ToUnixTimeMilliseconds();

            //if (this.pk == "CLT")
            //{
            //    this.pk = "qclt";
            //    this.Epoch = 9007199254740991; // Node.js
            //} 

            //if (this.pk == "BDL")
            //{
            //    this.pk = "qbdl";
            //    this.Epoch = 9223372036854775807; // Java
            //} 

            //if (this.pk == "SEA")
            //{
            //    this.pk = "qsea";
            //    this.Epoch = Int64.MaxValue; // DotNet, also 9223372036854775807
            //} 
        }
        
        public bool IsInCountry(string[] countryList)
        {
            try
            {
                foreach (var c in countryList) 
                {
                    if (Country.ToLower().Equals(c.ToLower()))
                    {
                        return true;
                    }
                }
            }
            catch (Exception) {
                return false;
            }
            return false;
        }

        public bool IsValid()
        {
            try {
                if (Math.Abs(AirportId) < 1) {
                    //Console.WriteLine("Invalid Airport - AirportId)");
                    return false;
                }
                if (String.IsNullOrEmpty(Name)) {
                    //Console.WriteLine("Invalid Airport - Name)");
                    return false;
                }
                if (String.IsNullOrEmpty(City)) {
                    //Console.WriteLine("Invalid Airport - City)");
                    return false;
                }
                if (String.IsNullOrEmpty(Country)) {
                    //Console.WriteLine("Invalid Airport - Country)");
                    return false;
                }
                if (String.IsNullOrEmpty(IataCode)) {
                    //Console.WriteLine("Invalid Airport - IataCode)");
                    return false;
                }
                if (String.IsNullOrEmpty(TimezoneCode)) {
                    //Console.WriteLine("Invalid Airport - TimezoneCode)");
                    return false;
                }
                if (Math.Abs(Latitude) < 0.00001) {
                    //Console.WriteLine("Invalid Airport - Latitude)");
                    return false;
                }
                if (Math.Abs(Longitude) < 0.00001) {
                    //Console.WriteLine("Invalid Airport - Longitude)");
                    return false;
                }
                if (Math.Abs(Latitude) > 179.99) {
                    //Console.WriteLine("Invalid Airport - Latitude)");
                    return false;
                }
                if (Math.Abs(Longitude) > 179.99) {
                    //Console.WriteLine("Invalid Airport - Longitude)");
                    return false;
                }
                if ((Altitude < -600) || (Altitude > 10000)) {
                    //Console.WriteLine("Invalid Airport - Altitude)");
                    return false;
                }
            }
            catch (Exception e) {
                Exception baseException = e.GetBaseException();
                Console.WriteLine("Error in IsValid: {0}, Message: {1}", e.Message, baseException.Message);
                return false;
            }
            return true;
        }

        public override string ToString()
        {
            bool valid = IsValid();
            return $"{AirportId}:{IataCode}:{Name}:{City}:{Country}:{Latitude}:{Longitude}:{TimezoneCode}:{TimezoneNum}:{valid}";
        }

        public string ToJson()
        {
            return JsonConvert.SerializeObject(this);
        }
    }
}
