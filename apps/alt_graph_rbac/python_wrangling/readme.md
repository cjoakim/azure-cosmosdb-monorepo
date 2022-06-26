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

### Example Edges - Modeled after RDF/Triplestore database "Triples"

The first two edge documents

```
{
  "id": "2ca8be4a-0633-41c5-b9ed-59afeb60fd7b",
  "doctype": "edge",
  "subject": "app1",
  "subject_doctype": "app",
  "subject_id": "9675e19f-f67d-4645-9bfe-f53f0a71e50d",
  "subject_pk": "app1",
  "predicate": "reader",
  "object": "app24",
  "object_doctype": "app",
  "object_id": "01ee532d-1413-4565-adff-6cfa016320ab",
  "object_pk": "app24"
}

{
  "id": "0540c5ae-1a03-42c4-9131-30c852ccfaab",
  "doctype": "edge",
  "subject": "app24",
  "subject_doctype": "app",
  "subject_id": "01ee532d-1413-4565-adff-6cfa016320ab",
  "subject_pk": "app24",
  "predicate": "read_by",
  "object": "app1",
  "object_doctype": "app",
  "object_id": "9675e19f-f67d-4645-9bfe-f53f0a71e50d",
  "object_pk": "app1"
}
```

---

## Execution


```
cd data/raw
./curl.sh

do minor edits of the two html files downloaded by curl, see comments in rbac_data.py

cd ../cc

python rbac_data.py parse_azure_rbac_docs_html

python rbac_data.py generate_cosmosdb_datasets 100

./generate_cosmosdb_load_files.sh
```

---

## Graph Visualization

### Cytoscape - a JavaScript graph visualization library

- https://js.cytoscape.org

#### ipycytoscape - Cytoscape in Jupyter Notebooks

- https://blog.jupyter.org/interactive-graph-visualization-in-jupyter-with-ipycytoscape-a8828a54ab63
- https://github.com/cytoscape/ipycytoscape
- https://github.com/cytoscape/ipycytoscape/tree/master/examples


