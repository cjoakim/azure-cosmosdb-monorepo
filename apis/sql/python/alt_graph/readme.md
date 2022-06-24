# azure-cosmosdb-monorepo - sql python alt_graph

## Graph Implementations with CosmosDB SQL

- **Bill of Material**
  - Based on this original repo with NPM library data
  - https://github.com/Azure-Samples/azure-cosmos-db-graph-npm-bom-sample 
  
- **RBAC, Role-Based-Access-Control**
  - Using simulated and actual data
  - https://docs.microsoft.com/en-us/azure/role-based-access-control/built-in-roles
    - file data/rbac/azure_roles.html
    - file data/rbac/azure_roles.json
  - https://docs.microsoft.com/en-us/azure/active-directory/roles/permissions-reference
    - file data/rbac/azure_ad_roles_permissions.html
    - file data/rbac/azure_ad_roles_permissions.json

## RBAC Data

  - See file data/rbac/generated_application_rbac_data.json
    - generated from the above two RBAC HTML pages and Python with Faker library.

### CosmosDB Implementation

- "Vertex" documents for the Applications
  - **pk** is app name, **doctype** is "app"
- "Vertex" documents for the People (owners, administrators, contributors)
  - **pk** is person name, **doctype** is "person"
- "Vertex" documents for the Azure Roles
  - **pk** is role name, **doctype** is "role", **role_type** is "Azure"
- "Vertex" documents for the Azure AD Roles
  - **pk** is role name, **doctype** is "role", **role_type** is "AD"
- "Vertex" documents for the Azure AD Permissions
  - **pk** is permission name, **doctype** is "permission"
- "Edge" documents as necessary to connect the above
- The Vertices have to exist before any Edges connecting them (thus ids and pks are known)
- **Composite Indexes** are created on the Vertex docs

### Triples

A **triple** is a data entity composed of **subject-predicate-object**, like "Bob is 35" or "Bob knows Fred".

See https://en.wikipedia.org/wiki/Triplestore

### Example Edge - Modeled after RDF/Triplestore database "Triples"

```
attribute:  example values

subject:    app1, Teresa Higgins
subject_id: <cosmosdb _id>
subject_pk: 
object:     
object_id:  
object_pk:  
predicate:  owner, administrator, contributor, reader_app, writer_app, etc 
```
