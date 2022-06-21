package org.cjoakim.cosmos.sql.spring_data_sql_gradle;

import com.azure.spring.data.cosmos.repository.CosmosRepository;
import com.azure.spring.data.cosmos.repository.Query;
import org.springframework.data.repository.query.Param;

import java.util.List;

// See https://docs.microsoft.com/en-us/azure/developer/java/spring-framework/how-to-guides-spring-data-cosmosdb

public interface AnnotatedQueriesUserRepositoryCodeSnippet extends CosmosRepository<User, String> {

    @Query("select * from c where c.firstName = @firstName and c.lastName = @lastName")
    List<User> getUsersByFirstNameAndLastName(@Param("firstName") String firstName, @Param("lastName") String lastName);

    @Query("select * from c offset @offset limit @limit")
    List<User> getUsersWithOffsetLimit(@Param("offset") int offset, @Param("limit") int limit);

    @Query("select value count(1) from c where c.firstName = @firstName")
    long getNumberOfUsersWithFirstName(@Param("firstName") String firstName);
}