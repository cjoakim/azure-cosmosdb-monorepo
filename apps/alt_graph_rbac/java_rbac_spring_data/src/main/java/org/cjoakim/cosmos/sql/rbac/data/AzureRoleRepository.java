package org.cjoakim.cosmos.sql.rbac.data;

import org.springframework.stereotype.Repository;
import com.azure.spring.data.cosmos.repository.CosmosRepository;

@Repository
public interface AzureRoleRepository extends CosmosRepository<AzureRole, String> {

    Iterable<AzureRole> findByDoctype(String doctype);
    long countByDoctype(String doctype);
}
