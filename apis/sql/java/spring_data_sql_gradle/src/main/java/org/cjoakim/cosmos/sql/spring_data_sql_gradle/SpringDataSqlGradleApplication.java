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

		logger.warn("uri: " + appConfiguration.getUri());

//		final User testUser = new User("testId", "testFirstName", "testLastName");
//
//		repository.deleteAll();
//		repository.save(testUser);
//
//		// to find by Id, please specify partition key value if collection is partitioned
//		final User result = repository.findOne(testUser.getId(), testUser.getLastName());
//
//		//  Switch to secondary key
//		UserRepositoryConfiguration bean =
//				applicationContext.getBean(UserRepositoryConfiguration.class);
//		bean.switchToSecondaryKey();
//
//		//  Now repository will use secondary key
//		repository.save(testUser);

	}
}
