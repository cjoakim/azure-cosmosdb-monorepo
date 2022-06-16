package org.cjoakim.azure.changefeed;

import com.azure.cosmos.*;
import com.azure.cosmos.implementation.guava25.collect.Lists;
import com.azure.cosmos.models.*;
import com.fasterxml.jackson.databind.JsonNode;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.CommandLineRunner;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.ComponentScan;
import reactor.core.scheduler.Schedulers;

import java.time.Duration;
import java.time.Instant;
import java.util.List;
import java.util.concurrent.atomic.AtomicBoolean;
import java.util.concurrent.atomic.AtomicInteger;

/**
 * This is the entry-point class for this Spring Boot application.
 * 
 * This code was adapted from https://github.com/Azure-Samples/azure-cosmos-java-sql-app-example
 * 
 * @author Chris Joakim, Microsoft
 * @date   2021/07/13
 */

@SpringBootApplication
@ComponentScan("org.cjoakim.azure")
public class App implements CommandLineRunner {

	private static final Logger logger = LoggerFactory.getLogger(App.class);

	@Autowired
	private AppConfig appConfig;
	
    private static AtomicBoolean isProcessorRunning = new AtomicBoolean(false);
    private static AtomicInteger counter = new AtomicInteger();
    private static ChangeFeedProcessor changeFeedProcessorInstance;
    
	public static void main(String[] args) {
		SpringApplication.run(App.class, args);
	}

	@Override
    public void run(String[] args) throws Exception {
    	
		String dbName = appConfig.getCosmosSqlDbname();
		String feedContainerName = appConfig.getCosmosSqlContainer();
		String leaseContainerName = feedContainerName + "-leases";
		
    	logger.info("cosmos uri:      " + appConfig.getCosmosSqlUri());
    	logger.info("cosmos key:      " + appConfig.getCosmosSqlKey().substring(0, 20) + "...");
    	logger.info("db:              " + dbName);
    	logger.info("feed container:  " + feedContainerName);
    	logger.info("lease container: " + leaseContainerName);
    	
    	CosmosAsyncClient client = null;
    	CosmosAsyncDatabase database = null;
    	CosmosAsyncContainer feedContainer = null;
    	CosmosAsyncContainer leaseContainer = null;
    	String hostName = "someName";
    	
    	if (true) {
    		try {
				client = getCosmosClient();
				logger.info("client:   " + client.toString());
				
				database = getDatabase(client, dbName);
				logger.info("database: " + database.getId());
				
				feedContainer = getContainer(client, dbName, feedContainerName);
				logger.info("feedContainer Id: " + feedContainer.getId());
				
				leaseContainer = createNewLeaseContainer(client, dbName, leaseContainerName);
				logger.info("leaseContainer Id: " + leaseContainer.getId());
				
	            changeFeedProcessorInstance = getChangeFeedProcessor(
	            		hostName, feedContainer, leaseContainer);
	            changeFeedProcessorInstance.start()
	                .subscribeOn(Schedulers.immediate())
	                .doOnSuccess(aVoid -> {
	                    isProcessorRunning.set(true);
	                    logger.warn("subscribe doOnSuccess");
	                })
	                .subscribe();

	            while (!isProcessorRunning.get());
			}
    		catch (Exception e) {
				e.printStackTrace();
				closeClient(client);
				throw e;
			}
    	}
    	//closeClient(client);
    }
	
    private CosmosAsyncClient getCosmosClient() {

        return new CosmosClientBuilder()
                .endpoint(appConfig.getCosmosSqlUri())
                .key(appConfig.getCosmosSqlKey())
                .consistencyLevel(ConsistencyLevel.SESSION)
                .contentResponseOnWriteEnabled(true)
				.multipleWriteRegionsEnabled(true)
				.preferredRegions(Lists.newArrayList("East US"))
				.connectionSharingAcrossClientsEnabled(false)
				.buildAsyncClient();
    }
    
    private static CosmosAsyncDatabase getDatabase(CosmosAsyncClient client, String dbName) {
    	
    	// Assuming that the DB already exists, but we could create it with the following line:
        // client.createDatabaseIfNotExists(dbName).block();
        return client.getDatabase(dbName);  
    }
    
	private static CosmosAsyncContainer getContainer(
			CosmosAsyncClient client, String dbName, String containerName) {
		
		CosmosAsyncDatabase databaseLink = client.getDatabase(dbName);
		logger.info("databaseLink Id: " + databaseLink.getId());
		return databaseLink.getContainer(containerName);
	}

	private static CosmosAsyncContainer createNewLeaseContainer(
		CosmosAsyncClient client, String dbName, String leaseContainerName) {

		CosmosAsyncDatabase databaseLink = client.getDatabase(dbName);
		logger.info("databaseLink Id: " + databaseLink.getId());
		
		CosmosAsyncContainer leaseContainerLink = databaseLink.getContainer(leaseContainerName);
		logger.info("leaseContainerLink Id: " + leaseContainerLink.getId());
		
		CosmosContainerResponse leaseContainerResponse = null;

		try {
			leaseContainerResponse = leaseContainerLink.read().block();
			if (leaseContainerResponse != null) {
				logger.info("deleting current leases container...");
				leaseContainerLink.delete().block();
				logger.info("leases container deleted");
				try {
					Thread.sleep(1000);
				}
				catch (InterruptedException ex) {
					ex.printStackTrace();
				}
			}
		}
		catch (RuntimeException ex) {
			if (ex instanceof CosmosException) {
				CosmosException cosmosClientException = (CosmosException) ex;
				if (cosmosClientException.getStatusCode() == 404) {
					logger.info("leases container not found");
				}
				else {
					throw ex;
				}
			}
			else {
				throw ex;
			}
		}

		CosmosContainerProperties containerSettings = 
				new CosmosContainerProperties(leaseContainerName, "/id");
		CosmosContainerRequestOptions requestOptions = 
				new CosmosContainerRequestOptions();
		ThroughputProperties throughputProperties = 
				ThroughputProperties.createManualThroughput(400);
		
		logger.info("creating leases container ...");
		leaseContainerResponse = databaseLink.createContainer(
			containerSettings, throughputProperties, requestOptions).block();

		if (leaseContainerResponse == null) {
			String msg = String.format("Failed to create container %s in database %s.", leaseContainerName);
			throw new RuntimeException(msg);
		}
		else {
			logger.info("leases container created");
		}
		return databaseLink.getContainer(leaseContainerName);
	}
    
    private ChangeFeedProcessor getChangeFeedProcessor(
		String hostName, CosmosAsyncContainer feedContainer, CosmosAsyncContainer leaseContainer) {
    	
        ChangeFeedProcessorOptions cfOptions = new ChangeFeedProcessorOptions();
        cfOptions.setFeedPollDelay(Duration.ofMillis(100));

		// When to start?  From the beginning, or from a specific point/Instant in time.
		boolean fromBeginning = false;
		if (fromBeginning) {
			cfOptions.setStartFromBeginning(true);
		}
		else {
			cfOptions.setStartFromBeginning(false);
			long seconds = 60 * 60 * 24 * 10;  // 10-days ago
			Instant startTime = Instant.now().minusSeconds(seconds);
			cfOptions.setStartTime(startTime);
			//com.azure.cosmos.CosmosException: Message:
			// {"Errors":["StartTime\/IfMofifiedSince is not currently supported when EnableMultipleWriteLocations is set."]}
		}

        return new ChangeFeedProcessorBuilder()
            .options(cfOptions)
            .hostName(hostName)
            .feedContainer(feedContainer)
            .leaseContainer(leaseContainer)
            .handleChanges((List<JsonNode> docs) -> {
                for (JsonNode document : docs) {
                	//System.out.println(document);
                	processFeedItem(document);
                }
            })
            .buildChangeFeedProcessor();
    }
    
    private void processFeedItem(JsonNode document) {
    	
    	int c = counter.addAndGet(1);
    	logger.info("processFeedItem; " + c + ": " + document);
    	
    	// TODO: do something more useful with the item other than just logging it
    }
    
	private void closeClient(CosmosAsyncClient client) {
		
		if (client != null) {
			logger.info("closeClient; closing...");
			client.close();
			logger.info("closeClient; closed");
			client = null;
		}
		else {
			logger.info("closeClient; client is null");
		}
	}
	
    private void deleteDatabase(CosmosAsyncDatabase db) {
    	
        db.delete().block();
    }
}
