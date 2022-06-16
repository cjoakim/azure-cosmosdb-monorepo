using System;
using System.IO;
using System.Collections.Generic;
using System.Text;
using System.Text.Json;
using System.Text.Json.Serialization;

// CosmosDB cost calculator console program.
//
// Usage:
//   dotnet run <your-input-specification-filename>
//   dotnet run specification1.txt
//   dotnet run specification2.txt
//
// Chris Joakim, Microsoft, 2020/10/31

namespace CJoakim.CosmosCalc
{
    class Program
    {
        static void Main(string[] args)
        {
            if (args.Length > 0)
            {
                // Read the lines of the spec file and pass the list to the SpecReader constructor.
                List<string> lines = new List<string>();
                using (var sr = new StreamReader(args[0]))
                { 
                    while (sr.Peek() >= 0)
                    {
                        lines.Add(sr.ReadLine().ToLower().Trim());
                    }
                }
                new SpecProcessor(lines).process();
            }
            else
            {
                Console.WriteLine("ERROR: no specification filename specified on the command-line.");
                Console.WriteLine("Usage:");
                Console.WriteLine("  dotnet run <your-input-specification-filename>");
                Console.WriteLine("  dotnet run specification1.txt");
            }
        }
    }
}
