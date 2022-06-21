package org.cjoakim.cosmos.sql.spring_data_sql_gradle;

import com.azure.spring.data.cosmos.repository.Query;
import com.azure.spring.data.cosmos.repository.ReactiveCosmosRepository;
import com.fasterxml.jackson.databind.node.ObjectNode;
import org.springframework.data.repository.query.Param;
import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;

// See https://docs.microsoft.com/en-us/azure/developer/java/spring-framework/how-to-guides-spring-data-cosmosdb
// See https://github.com/Azure/azure-sdk-for-java/blob/spring-cloud-azure_4.2.0/sdk/cosmos/azure-spring-data-cosmos/src/samples/java/com/azure/spring/data/cosmos/AnnotatedQueriesUserReactiveRepositoryCodeSnippet.java

public interface AnnotatedQueriesUserReactiveRepositoryCodeSnippet
        extends ReactiveCosmosRepository<User, String> {

    @Query("select * from c where c.firstName = @firstName and c.lastName = @lastName")
    Flux<User> getUsersByTitleAndValue(@Param("firstName") int firstName, @Param("lastName") String lastName);

    @Query("select * from c offset @offset limit @limit")
    Flux<User> getUsersWithOffsetLimit(@Param("offset") int offset, @Param("limit") int limit);

    @Query("select count(c.id) as num_ids, c.lastName from c group by c.lastName")
    Flux<ObjectNode> getCoursesGroupByDepartment();

    @Query("select value count(1) from c where c.lastName = @lastName")
    Mono<Long> getNumberOfUsersWithLastName(@Param("lastName") String lastName);
}