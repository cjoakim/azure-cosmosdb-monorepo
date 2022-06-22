package org.cjoakim.cosmos.sql.spring_data_sql_gradle;

import com.azure.spring.data.cosmos.repository.CosmosRepository;
import org.springframework.stereotype.Repository;

// See https://docs.microsoft.com/en-us/azure/developer/java/spring-framework/how-to-guides-spring-data-cosmosdb
// See https://github.com/Azure/azure-sdk-for-java/blob/spring-cloud-azure_4.2.0/sdk/cosmos/azure-spring-data-cosmos/src/samples/java/com/azure/spring/data/cosmos/UserRepository.java

@Repository
public interface UserRepository extends CosmosRepository<User, String> {

//    Iterable<User> findByFirstName(String firstName);
//
//    long countByFirstName(String firstName);
//
//    User findOne(String id, String lastName);
}
