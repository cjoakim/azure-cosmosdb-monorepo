# events notebook

This file contains the PySpark Notebook code in markdown format, rather than ipynb,
for easy copy-and-paste into your Notebook.

---

## Cell 1

### Code

```
df = spark.read\
    .format("cosmos.olap")\
    .option("spark.synapse.linkedService", "cjoakimiotcosmossql_dev")\
    .option("spark.cosmos.container", "events")\
    .load()

df.printSchema()
```

### Output

#### IoT Events

```
root
 |-- _rid: string (nullable = true)
 |-- _ts: long (nullable = true)
 |-- seq: long (nullable = true)
 |-- epoch: double (nullable = true)
 |-- device_type: string (nullable = true)
 |-- device_os: string (nullable = true)
 |-- device_version: string (nullable = true)
 |-- device_pid: long (nullable = true)
 |-- line_speed: long (nullable = true)
 |-- temperature: long (nullable = true)
 |-- humidity: long (nullable = true)
 |-- EventProcessedUtcTime: string (nullable = true)
 |-- PartitionId: long (nullable = true)
 |-- EventEnqueuedUtcTime: string (nullable = true)
 |-- IoTHub: struct (nullable = true)
 |    |-- MessageId: string (nullable = true)
 |    |-- CorrelationId: string (nullable = true)
 |    |-- ConnectionDeviceId: string (nullable = true)
 |    |-- ConnectionDeviceGenerationId: string (nullable = true)
 |    |-- EnqueuedTime: string (nullable = true)
 |    |-- StreamId: integer (nullable = true)
 |-- pk: string (nullable = true)
 |-- id: string (nullable = true)
 |-- _etag: string (nullable = true)
```

#### Airport Events

```
root
 |-- _rid: string (nullable = true)
 |-- _ts: long (nullable = true)
 |-- id: string (nullable = true)
 |-- pk: string (nullable = true)
 |-- AirportId: long (nullable = true)
 |-- Name: string (nullable = true)
 |-- City: string (nullable = true)
 |-- Country: string (nullable = true)
 |-- IataCode: string (nullable = true)
 |-- IcaoCode: string (nullable = true)
 |-- Latitude: double (nullable = true)
 |-- Longitude: double (nullable = true)
 |-- location: struct (nullable = true)
 |    |-- type: string (nullable = true)
 |    |-- coordinates: array (nullable = true)
 |    |    |-- element: double (containsNull = true)
 |-- Altitude: long (nullable = true)
 |-- TimezoneNum: double (nullable = true)
 |-- Dst: string (nullable = true)
 |-- TimezoneCode: string (nullable = true)
 |-- _etag: string (nullable = true)
 |-- Epoch: long (nullable = true)
```

---

## Cell 2

### Code

```
display(df.limit(100))
```

---

## Cell 3

### Code

#### Implementation with simulated IoT events:

```
from pyspark.sql import functions as f

recent_df = df.select("pk","line_speed","temperature","humidity", "epoch").filter("epoch >= 1603986247").sort("epoch", ascending=False) 
display(recent_df.limit(10))
```

#### Alternative implementation with Airport events:

```
from pyspark.sql import functions as f

belgian_df = df.select("_ts", "Epoch", "pk", "City", "Country", "Name")\
    .filter("_ts >= 1618846698 and Country = 'Belgium'")\
    .sort("_ts", ascending=False) 

display(belgian_df.limit(10))
```

Corresponding CosmosDB SQL Query:

```
select c._ts, c.Epoch, c.pk, c.City, c.Country, c.Name from c where c.Country = 'Belgium' and c._ts > 1618846698 order by c._ts desc
```

---

## Cell 4

### Code


```
from pyspark.sql import functions as f

latest_df = df.select("_ts", "Epoch", "pk", "City", "Country", "Name")\
    .filter("_ts >= 1618846698")\
    .sort("_ts", ascending=False) 

display(latest_df.limit(10))
```
