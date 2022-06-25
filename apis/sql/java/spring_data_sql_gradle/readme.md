# azure-cosmosdb-monorepo - spring_data_sql_gradle

## Spring Data Links

- https://docs.microsoft.com/en-us/java/api/overview/azure/spring-data-cosmos-readme?view=azure-java-stable
- https://docs.microsoft.com/en-us/azure/developer/java/spring-framework/how-to-guides-spring-data-cosmosdb


## azure-spring-data-cosmos library

- https://search.maven.org/artifact/com.azure/azure-spring-data-cosmos   (Maven Central)
- https://search.maven.org/artifact/com.azure/azure-spring-data-cosmos/3.22.0/jar  (Maven Central)
- https://github.com/Azure/azure-sdk-for-java/tree/main/sdk/cosmos/azure-spring-data-cosmos  (SDK and Samples)
- https://github.com/Azure/azure-sdk-for-java/blob/spring-cloud-azure_4.2.0/sdk/cosmos/azure-spring-data-cosmos/src/samples/java/com/azure/spring/data/cosmos/SampleApplication.java

---

## This Application

### Primary files

```
build.gradle
  The Gradle application build and configuration file, contains dependencies, including:
  com.azure.spring:spring-cloud-azure-starter-data-cosmos

src/main/resources/application.properties
  Configuration and environment variables

src/main/java/org/cjoakim/cosmos/sql/spring_data_sql_gradle/User.java
  An annotated POJO domain class.  Maps to the CosmosDB users container with this annotation:
  @Container(containerName="users")

src/main/java/org/cjoakim/cosmos/sql/spring_data_sql_gradle/UserRepository.java
  A Spring Data "Repository" class pointing to CosmosDB

src/main/java/org/cjoakim/cosmos/sql/spring_data_sql_gradle/App.java
  Entry point to the application, see the main() and run() methods.
  Constructs instances of class User, and persists/updates/queries them
  with class UserRepository
```

### Build and Execute

```
gradle build

gradle bootRun --args='--delete-all'
```

### Sample Document

Note the nesting in the "other" attribute; see User.java

```
{
    "id": "9283d85f-3200-419a-b5cf-4f52fde15ae0",
    "pk": "Joakim",
    "firstName": "Miles",
    "other": {
        "id": "612e4e91-3295-4a20-aa0d-aef172b9a2e7",
        "pk": "Joakim",
        "firstName": "Elsa",
        "other": {
            "id": "4e60506e-523b-47ef-b24b-8f1c58d378f3",
            "pk": "Joakim",
            "firstName": "Chris",
            "other": null,
            "lastName": "Joakim"
        },
        "lastName": "Joakim"
    },
    "lastName": "Joakim",
    "_rid": "gklzAI3Er5pJAAAAAAAAAA==",
    "_self": "dbs/gklzAA==/colls/gklzAI3Er5o=/docs/gklzAI3Er5pJAAAAAAAAAA==/",
    "_etag": "\"7200bdf7-0000-0100-0000-62b75f850000\"",
    "_attachments": "attachments/",
    "_ts": 1656184709
}
```