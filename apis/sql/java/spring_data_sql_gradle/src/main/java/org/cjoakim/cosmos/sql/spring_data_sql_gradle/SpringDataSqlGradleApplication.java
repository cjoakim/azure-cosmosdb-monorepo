package org.cjoakim.cosmos.sql.spring_data_sql_gradle;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.CommandLineRunner;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.ApplicationContext;

//@SpringBootApplication
//public class SpringDataSqlGradleApplication {
//
//	public static void main(String[] args) {
//		SpringApplication.run(SpringDataSqlGradleApplication.class, args);
//	}
//
//}

// See https://docs.microsoft.com/en-us/azure/developer/java/spring-framework/how-to-guides-spring-data-cosmosdb
// See https://github.com/Azure/azure-sdk-for-java/blob/spring-cloud-azure_4.2.0/sdk/cosmos/azure-spring-data-cosmos/src/samples/java/com/azure/spring/data/cosmos/SampleApplication.java

@SpringBootApplication
public class SpringDataSqlGradleApplication implements CommandLineRunner {

	private static final Logger logger = LoggerFactory.getLogger(SpringDataSqlGradleApplication.class);

	@Autowired
	private UserRepository repository;

	@Autowired
	private ApplicationContext applicationContext;

	@Autowired
	private AppConfiguration appConfiguration;

	public static void main(String[] args) {
		SpringApplication.run(SpringDataSqlGradleApplication.class, args);
	}

	public void run(String... var1) {
		logger.warn("start of run() method");

		boolean deleteAll = false;
		logger.warn("deleteAll: " + deleteAll);

		if (deleteAll) {
			logger.warn("deleteAll starting");
			repository.deleteAll();
			logger.warn("deleteAll completed");
		}

		final User testUser1 = new User(
				"" + System.currentTimeMillis(),
				"George",
				"Foreman");
		logger.warn("testUser1 created: " + testUser1);

		repository.save(testUser1);
		logger.warn("testUser1 saved");

		logger.warn("spring app exiting");
		SpringApplication.exit(this.applicationContext);
		logger.warn("spring app exit completed");
	}
}
