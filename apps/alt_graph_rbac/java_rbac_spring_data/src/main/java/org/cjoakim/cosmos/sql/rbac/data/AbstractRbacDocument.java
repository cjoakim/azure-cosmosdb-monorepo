package org.cjoakim.cosmos.sql.rbac.data;

import com.azure.spring.data.cosmos.core.mapping.Container;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.extern.slf4j.Slf4j;

@Container(containerName = "rbac")
@NoArgsConstructor
@AllArgsConstructor
@Data
@Slf4j
public abstract class AbstractRbacDocument {

    private String id;
    private String pk;
    private String doctype;
}

//{"id": "b24988ac-6180-42a0-ab88-20f7382dd24c", "doctype": "azure_role", "pk": "Contributor",
// "role": "Contributor", "href": "contributor", "desc": "Grants full access to manage all resources, but does not allow you to assign roles in Azure RBAC, manage assignments in Azure Blueprints, or share image galleries."}
