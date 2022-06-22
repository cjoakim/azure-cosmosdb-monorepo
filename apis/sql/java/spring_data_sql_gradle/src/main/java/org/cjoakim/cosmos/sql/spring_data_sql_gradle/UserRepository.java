package org.cjoakim.cosmos.sql.spring_data_sql_gradle;

import com.azure.spring.data.cosmos.repository.CosmosRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface UserRepository extends CosmosRepository<User, String> {

//    Iterable<User> findByFirstName(String firstName);
//
//    long countByFirstName(String firstName);
//
//    User findOne(String id, String lastName);
}
