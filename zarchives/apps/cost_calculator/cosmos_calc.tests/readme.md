# Unit Testing Notes

```
$ dotnet test --collect:"XPlat Code Coverage"

... created file TestResults/f036d7c6-59b9-4e48-8d9d-ef368fac60bb/coverage.cobertura.xml
```

## Install dotnet-reportgenerator-globaltool

```
$ dotnet tool install -g dotnet-reportgenerator-globaltool
```

On macOS, this installs the tool to your ~/.dotnet/tools directory.  Add this directory to your $PATH.
```