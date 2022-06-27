package org.cjoakim.cosmos.sql.rbac.data;

import com.azure.spring.data.cosmos.repository.CosmosRepository;
import com.azure.spring.data.cosmos.repository.Query;
import org.cjoakim.cosmos.sql.rbac.data.User;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface UserRepository extends CosmosRepository<User, String> {

    Iterable<User> findByFirstName(String firstName);
    long countByLastName(String lastName);
    //User findOne(String id, String firstName);

    // See https://github.com/Azure-Samples/azure-spring-data-cosmos-java-sql-api-samples/blob/main/src/main/java/com/azure/cosmos/springexamples/quickstart/sync/UserRepository.java#
    @Query(value = "SELECT * FROM c WHERE c.pk = @pk")
    List<User> getUsersInPk(@Param("pk") String pk);
}
