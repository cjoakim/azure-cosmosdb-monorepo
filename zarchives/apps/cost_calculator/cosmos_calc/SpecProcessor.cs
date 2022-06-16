using System;
using System.IO;

using System.Collections.Generic;
using System.Text;
using System.Text.Json;
using System.Text.Json.Serialization;

// Instances of this class are created in Program.cs and are used to read
// and process a given spec file.
// Chris Joakim, Microsoft, 2020/10/31

namespace CJoakim.CosmosCalc
{
    public class SpecProcessor
    {
        // Instance variables:
        public Container currentContainer { get; set; }

        //The following two are used for unit testing:
        public List<string> specLines { get; set; }  
        public List<string> calculationResults { get; set; }  

        public SpecProcessor(List<string> lines)
        {
            this.specLines = lines;
            this.currentContainer = null;
            this.calculationResults = new List<string>();
        }

        public void process()
        {
            Container currentContainer = null; 

            foreach (string line in specLines)
            {
                string[] tokens = line.Split(':');
                if (tokens.Length == 2)
                {
                    string key = tokens[0].Trim();
                    string value = tokens[1].Trim();

                    switch (key) {             
                        case "container": 
                            currentContainer = new Container();
                            currentContainer.name = value;
                            break; 
                        case "provisioning_type": 
                            currentContainer.provisioningType = value;
                            break; 
                        case "replication_type": 
                            currentContainer.replicationType = value;
                            break; 
                        case "ru_per_second":
                            currentContainer.ruPerSecond = Int32.Parse(value);
                            break;
                        case "region_count":
                            currentContainer.regionCount = Int32.Parse(value);
                            break;
                        case "availability_zone":
                            if (value == "true") {
                                currentContainer.availabilityZone = true;
                            }
                            if (value == "false") {
                                currentContainer.availabilityZone = false;
                            }    
                            break; 
                        case "size_in_bytes": 
                            currentContainer.SetSizeInBytes(Int64.Parse(value));
                            break; 
                        case "size_in_mb": 
                            currentContainer.SetSizeInMB(Double.Parse(value));
                            break; 
                        case "size_in_gb": 
                            currentContainer.sizeInGB = Double.Parse(value);
                            break; 
                        case "size_in_tb": 
                            currentContainer.SetSizeInTB(Double.Parse(value));
                            break;
                        case "size_in_pb": 
                            currentContainer.SetSizeInPB(Double.Parse(value));
                            break;  
                        case "max_historical_manual_ru": 
                            currentContainer.maxHistoricalManualRu = Int32.Parse(value);
                            break; 
                        case "max_historical_auto_ru": 
                            currentContainer.maxHistoricalAutoRu = Int32.Parse(value);
                            break;
                        case "replicated_gb_per_month":
                            currentContainer.replicatedGBPerMonth = (Double.Parse(value));
                            break;
                        case "synapse_link_enabled":
                            if (value == "true")
                            {
                                currentContainer.synapseLinkEnabled = true;
                            }
                            if (value == "false")
                            {
                                currentContainer.synapseLinkEnabled = false;
                            }
                            break;

                        // The above case statements 'set' the state of the container, while
                        // the following case statement is used to trigger calculations.

                        case "calculate_costs":
                            if (value == "true")
                            {
                                double costs = currentContainer.CalculateCosts();
                                var options = new JsonSerializerOptions
                                {
                                    WriteIndented = true,
                                };
                                string result = JsonSerializer.Serialize(currentContainer, options);
                                calculationResults.Add(result);
                                Console.WriteLine(result);
                            }
                            break; 

                        default: 
                            Console.WriteLine("WARNING: unrecognized statement - " + key); 
                            break;
                    }
                }
            }
        }
    }
}
