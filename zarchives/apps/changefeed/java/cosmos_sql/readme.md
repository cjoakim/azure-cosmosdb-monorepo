# azure-cosmosdb-changefeed

Consume the **CosmosDB/SQL API** Change-Feed with **Java**

[Bootstrapping this Spring Boot Project](boot-project.md)

## Links

- https://docs.microsoft.com/en-us/azure/cosmos-db/change-feed-processor
- https://docs.microsoft.com/en-us/azure/cosmos-db/create-sql-api-java-changefeed
- https://docs.microsoft.com/en-us/azure/cosmos-db/sql-api-sdk-java-v4
- https://docs.microsoft.com/en-us/java/api/overview/azure/cosmos-readme?view=azure-java-stable
- https://medium.com/walmartglobaltech/azure-cosmos-change-feed-processor-for-java-3e784ac6ef07
- [Spring Initializr](https://start.spring.io/)

See Sample repo:
```
git clone https://github.com/Azure-Samples/azure-cosmos-java-sql-app-example.git
```

## Implementation Notes

**Java 11** and **Apache Maven 3** are used in this project.

The **Spring Boot** framework is used in this implementation, but only for core functionality
like configuration and logging.  The Spring Data framework is not used.  

The **CosmosDB Java SDK version 4** is used, per this pom.xml entry:

```
    <!-- CosmosDB SDK - https://mvnrepository.com/artifact/com.azure/azure-cosmos -->
    <dependency>
        <groupId>com.azure</groupId>
        <artifactId>azure-cosmos</artifactId>
        <version>4.0.1</version> <!-- 4.13.0 4.0.1  -->
    </dependency>
```

This sample program simply logs the change feed events and does no additional processing
with them.

## Build

```
$ cd changefeed/
./build.sh

or

$ mvn clean compile package -Dmaven.test.skip=true
```

## Run 

The following **environment variables** are expected to be present, 
see your Azure Portal for their values.

```
AZURE_COSMOSDB_SQLDB_DBNAME        <-- your database name in your cosmosdb account
AZURE_COSMOSDB_SQLDB_COLLNAME      <-- your container within the database, such as "amtrak"
AZURE_COSMOSDB_SQLDB_KEY
AZURE_COSMOSDB_SQLDB_URI
```

This sample program program will **delete and recreate the appropriate leases container**.
The leases container name will be your given container name plus "-leases" appended
to the end.  For example: **amtrak** and **amtrak-leases**.

```
$ ./run.sh

or 

$ java -Xmx200m -Ddebug=true -Dspring.profiles.active=default -jar target/changefeed-0.0.1.jar consume
```

Sample output:

```
[INFO] ------------------------------------------------------------------------
[INFO] BUILD SUCCESS
[INFO] ------------------------------------------------------------------------
...

  .   ____          _            __ _ _
 /\\ / ___'_ __ _ _(_)_ __  __ _ \ \ \ \
( ( )\___ | '_ | '_| | '_ \/ _` | \ \ \ \
 \\/  ___)| |_)| | | | | || (_| |  ) ) ) )
  '  |____| .__|_| |_|_| |_\__, | / / / /
 =========|_|==============|___/=/_/_/_/
 :: Spring Boot ::        (v2.3.9.RELEASE)

08:53:37.341 INFO  o.cjoakim.azure.changefeed.App - Starting App v0.0.1 on christohersimac.lan with PID 13220 (/Users/cjoakim/github/azure-cosmosdb-changefeed/java/cosmos_sql/changefeed/target/changefeed-0.0.1.jar started by cjoakim in /Users/cjoakim/github/azure-cosmosdb-changefeed/java/cosmos_sql/changefeed)
08:53:37.342 DEBUG o.cjoakim.azure.changefeed.App - Running with Spring Boot v2.3.9.RELEASE, Spring v5.2.13.RELEASE
08:53:37.342 INFO  o.cjoakim.azure.changefeed.App - The following profiles are active: default
08:53:37.342 DEBUG o.s.boot.SpringApplication - Loading source class org.cjoakim.azure.changefeed.App
08:53:37.420 DEBUG o.s.b.c.c.ConfigFileApplicationListener - Activated activeProfiles default
08:53:37.420 DEBUG o.s.b.c.c.ConfigFileApplicationListener - Loaded config file 'jar:file:/Users/cjoakim/github/azure-cosmosdb-changefeed/java/cosmos_sql/changefeed/target/changefeed-0.0.1.jar!/BOOT-INF/classes!/application.properties' (classpath:/application.properties)
08:53:38.013 INFO  o.cjoakim.azure.changefeed.App - Started App in 1.136 seconds (JVM running for 1.606)
08:53:38.019 INFO  o.cjoakim.azure.changefeed.App - cosmos uri:      https://cjoakimcosmossql.documents.azure.com:443/
08:53:38.023 INFO  o.cjoakim.azure.changefeed.App - cosmos key:      ...secret...
08:53:38.023 INFO  o.cjoakim.azure.changefeed.App - db:              dev
08:53:38.023 INFO  o.cjoakim.azure.changefeed.App - feed container:  amtrak
08:53:38.023 INFO  o.cjoakim.azure.changefeed.App - lease container: amtrak-leases
08:53:39.813 INFO  o.cjoakim.azure.changefeed.App - client:   com.azure.cosmos.CosmosAsyncClient@39a8312f
08:53:39.813 INFO  o.cjoakim.azure.changefeed.App - database: dev
08:53:39.814 INFO  o.cjoakim.azure.changefeed.App - databaseLink Id: dev
08:53:39.814 INFO  o.cjoakim.azure.changefeed.App - feedContainer Id: amtrak
08:53:39.814 INFO  o.cjoakim.azure.changefeed.App - databaseLink Id: dev
08:53:39.815 INFO  o.cjoakim.azure.changefeed.App - leaseContainerLink Id: amtrak-leases
08:53:40.548 INFO  o.cjoakim.azure.changefeed.App - deleting current leases container...
08:53:41.530 INFO  o.cjoakim.azure.changefeed.App - leases container deleted
08:53:42.542 INFO  o.cjoakim.azure.changefeed.App - creating leases container ...
08:53:45.424 INFO  o.cjoakim.azure.changefeed.App - leases container created
08:53:45.425 INFO  o.cjoakim.azure.changefeed.App - leaseContainer Id: amtrak-leases
08:54:05.762 WARN  o.cjoakim.azure.changefeed.App - subscribe doOnSuccess
08:54:10.993 INFO  o.cjoakim.azure.changefeed.App - processFeedItem; 1: {"station_code_sequence":"WAS,NCR,BWI,BAL,ABE,NRK,WIL,PHL,PHN,CWH,TRE,PJC,NBK,MET,EWR,NWK,NYP,NRO,STM,BRP,NHV,OSB,NLC,MYS,WLY,KIN,PVD,RTE,BBY","station_count":29,"station_list":["WAS: Washington, District of Columbia","NCR: New Carrollton, Maryland","BWI: BWI Rail Station at Thurgood Marshall Airport, Mar","BAL: Baltimore (Penn Station), Maryland","ABE: Aberdeen, Maryland","NRK: Newark, Delaware","WIL: Wilmington, Delaware","PHL: Philadelphia, Pennsylvania","PHN: Philadelphia (North), Pennsylvania","CWH: Cornwells Heights, Pennsylvania","TRE: Trenton, New Jersey","PJC: Princeton Junction, New Jersey","NBK: New Brunswick, New Jersey","MET: Metropark (Iselin), New Jersey","EWR: Newark Liberty International Airport, New Jersey","NWK: Newark (Penn Station), New Jersey","NYP: New York (Penn Station), New York","NRO: New Rochelle, New York","STM: Stamford, Connecticut","BRP: Bridgeport, Connecticut","NHV: New Haven, Connecticut","OSB: Old Saybrook, Connecticut","NLC: New London, Connecticut","MYS: Mystic, Connecticut","WLY: Westerly, Rhode Island","KIN: West Kingston, Rhode Island","PVD: Providence, Rhode Island","RTE: Westwood, Route 128 Station, Massachusetts","BBY: Boston (Back Bay), Massachusetts"],"distance":421,"pk":"Acela","doctype":"route","epoch":1616088366,"id":"d5e26a0d-f848-4c8a-bd9f-ee2de1ed7722","_rid":"5IsfAOaDIasBAAAAAAAAAA==","_self":"dbs/5IsfAA==/colls/5IsfAOaDIas=/docs/5IsfAOaDIasBAAAAAAAAAA==/","_etag":"\"030097d3-0000-0100-0000-60538d2f0000\"","_attachments":"attachments/","_ts":1616088367,"_lsn":2}

08:54:10.994 INFO  o.cjoakim.azure.changefeed.App - processFeedItem; 2: {"station_code_sequence":"NYP,YNY,CRT,POU,RHI,HUD,ALB,SDY,SAR,FED,WHL,FTC,POH,WSP,PRK,PLB,RSP","station_count":17,"station_list":["NYP: New York (Penn Station), New York","YNY: Yonkers, New York","CRT: Croton Harmon, New York","POU: Poughkeepsie, New York","RHI: Rhinecliff, New York","HUD: Hudson, New York","ALB: Albany/Rensselaer, New York","SDY: Schenectady, New York","SAR: Saratoga Springs, New York","FED: Fort Edward-Glens Falls, New York","WHL: Whitehall, New York","FTC: Ticonderoga, New York","POH: Port Henry, New York","WSP: Westport, New York","PRK: Port Kent, New York","PLB: Plattsburgh, New York","RSP: Rouses Point, New York"],"distance":309,"pk":"Adirondack","doctype":"route","epoch":1616088367,"id":"1620d07d-3f08-4272-8783-36e532b48c0e","_rid":"5IsfAOaDIasCAAAAAAAAAA==","_self":"dbs/5IsfAA==/colls/5IsfAOaDIas=/docs/5IsfAOaDIasCAAAAAAAAAA==/","_etag":"\"030098d3-0000-0100-0000-60538d2f0000\"","_attachments":"attachments/","_ts":1616088367,"_lsn":3}

08:54:10.994 INFO  o.cjoakim.azure.changefeed.App - processFeedItem; 3: {"station_code_sequence":"SFA,DLD,PAK,JAX,JSP,SAV,YEM,CHS,KTR,FLO,DIL,FAY,SSM,WLN,RMT,PTB,RVR,ASD,FBG,QAN,WDB,LOR","station_count":22,"station_list":["SFA: Sanford, Florida","DLD: Deland, Florida","PAK: Palatka, Florida","JAX: Jacksonville, Florida","JSP: Jesup, Georgia","SAV: Savannah, Georgia","YEM: Yemassee, South Carolina","CHS: Charleston, South Carolina","KTR: Kingstree, South Carolina","FLO: Florence, South Carolina","DIL: Dillon, South Carolina","FAY: Fayetteville, North Carolina","SSM: Selma, North Carolina","WLN: Wilson, North Carolina","RMT: Rocky Mount, North Carolina","PTB: Petersburg, Virginia","RVR: Richmond (Staples Mill Rd), Virginia","ASD: Ashland, Virginia","FBG: Fredericksburg, Virginia","QAN: Quantico, Virginia","WDB: Woodbridge, Virginia","LOR: Lorton (Auto Train), Virginia"],"distance":804,"pk":"Auto Train","doctype":"route","epoch":1616088367,"id":"1a529787-e570-4f4a-9456-962490eabb9d","_rid":"5IsfAOaDIasDAAAAAAAAAA==","_self":"dbs/5IsfAA==/colls/5IsfAOaDIas=/docs/5IsfAOaDIasDAAAAAAAAAA==/","_etag":"\"030099d3-0000-0100-0000-60538d2f0000\"","_attachments":"attachments/","_ts":1616088367,"_lsn":4}
...

```


## Reference Repo

```
git clone https://github.com/Azure-Samples/azure-cosmos-java-sql-app-example.git
```
