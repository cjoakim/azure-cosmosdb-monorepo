# 

## Java SDK: Azure Cognitive Search client library for Java

- https://docs.microsoft.com/en-us/java/api/overview/azure/search-documents-readme?view=azure-java-stable
- https://search.maven.org/artifact/com.azure/azure-search-documents/11.4.5/jar

### Examples

- https://github.com/Azure/azure-sdk-for-java


---

## This Example Project

### Environment Variables

The following are assumed to be present on your system:
```
TODO
```

### Project Setup With Gradle 

See https://docs.gradle.org/7.3/userguide/building_java_projects.html

```
$ gradle init
Starting a Gradle Daemon (subsequent builds will be faster)

Select type of project to generate:
  1: basic
  2: application
  3: library
  4: Gradle plugin
Enter selection (default: basic) [1..4] 2

Select implementation language:
  1: C++
  2: Groovy
  3: Java
  4: Kotlin
  5: Scala
  6: Swift
Enter selection (default: Java) [1..6] 3

Split functionality across multiple subprojects?:
  1: no - only one application project
  2: yes - application and library projects
Enter selection (default: no - only one application project) [1..2] 1

Select build script DSL:
  1: Groovy
  2: Kotlin
Enter selection (default: Groovy) [1..2] 1

Generate build using new APIs and behavior (some features may change in the next minor release)? (default: no)

Select test framework:
  1: JUnit 4
  2: TestNG
  3: Spock
  4: JUnit Jupiter
Enter selection (default: JUnit Jupiter) [1..4] 1

Project name (default: sdk_client):
Source package (default: sdk_client): org.cjoakim.azure.cogsearch

> Task :init
Get more help with your project: https://docs.gradle.org/7.3/samples/sample_building_java_applications.html

BUILD SUCCESSFUL in 1m 16s
2 actionable tasks: 2 executed
```

Then add the following to **build.gradle**

```
    implementation 'com.azure:azure-search-documents:11.4.5'
```