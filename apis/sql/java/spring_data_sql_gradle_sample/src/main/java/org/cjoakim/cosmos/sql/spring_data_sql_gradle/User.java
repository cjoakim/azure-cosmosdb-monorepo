package org.cjoakim.cosmos.sql.spring_data_sql_gradle;

import com.azure.spring.data.cosmos.core.mapping.Container;
import com.azure.spring.data.cosmos.core.mapping.CosmosUniqueKey;
import com.azure.spring.data.cosmos.core.mapping.CosmosUniqueKeyPolicy;
import com.azure.spring.data.cosmos.core.mapping.PartitionKey;

// See https://docs.microsoft.com/en-us/azure/developer/java/spring-framework/how-to-guides-spring-data-cosmosdb
// See https://github.com/Azure/azure-sdk-for-java/blob/spring-cloud-azure_4.2.0/sdk/cosmos/azure-spring-data-cosmos/src/samples/java/com/azure/spring/data/cosmos/User.java

@Container(containerName="users")  //, autoScale=true, ru="4000")
//@CosmosUniqueKeyPolicy(uniqueKeys = {
//        @CosmosUniqueKey(paths = {"/lastName", "/zipCode"}),
//        @CosmosUniqueKey(paths = {"/city"})
//})
public class User {
    private String id;
    private String pk;
    private String firstName;


    @PartitionKey
    private String lastName;

    public User() {
        // If you do not want to create a default constructor,
        // use annotation @JsonCreator and @JsonProperty in the full args constructor
    }

    public User(String id, String firstName, String lastName) {
        this.id = id;
        this.firstName = firstName;
        this.lastName  = lastName;
        this.pk        = this.lastName;
    }

    @Override
    public String toString() {
        return String.format("User: %s %s, %s", firstName, lastName, id);
    }

    public String getId() {
        return id;
    }

    public void setId(String id) {
        this.id = id;
    }

    public String getFirstName() {
        return firstName;
    }

    public void setFirstName(String firstName) {
        this.firstName = firstName;
    }

    public String getLastName() {
        return lastName;
    }

    public void setLastName(String lastName) {
        this.lastName = lastName;
        this.pk = this.lastName;
    }

    public String getPk() {
        return pk;
    }

    public void setPk(String pk) {
        this.pk = pk;
    }
}
