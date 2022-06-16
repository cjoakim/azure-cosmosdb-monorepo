#!/bin/bash

# Execute the Xunit unit tests (on linux/macos), then produce code coverage reports with reportgenerator.
# Chris Joakim, Microsoft, 2020/10/31

# dotnet test -t
# dotnet test -t | grep Egress

#dotnet test --filter "FullyQualifiedName=cosmos_calc.tests.ContainerEgressTest.TestEgress"

dotnet test --filter "FullyQualifiedName=cosmos_calc.tests.SpecProcessorTest.Spec3MB_Autoscale_InMB_Test"
