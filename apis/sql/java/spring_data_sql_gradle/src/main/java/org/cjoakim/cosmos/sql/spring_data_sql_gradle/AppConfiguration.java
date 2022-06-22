package org.cjoakim.cosmos.sql.spring_data_sql_gradle;

import com.azure.core.credential.AzureKeyCredential;
import com.azure.cosmos.CosmosClientBuilder;
import com.azure.cosmos.DirectConnectionConfig;
import com.azure.cosmos.GatewayConnectionConfig;
import com.azure.spring.data.cosmos.config.AbstractCosmosConfiguration;
import com.azure.spring.data.cosmos.config.CosmosConfig;
import com.azure.spring.data.cosmos.core.ResponseDiagnostics;
import com.azure.spring.data.cosmos.core.ResponseDiagnosticsProcessor;
import com.azure.spring.data.cosmos.repository.config.EnableCosmosRepositories;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.lang.Nullable;

// See https://docs.microsoft.com/en-us/azure/developer/java/spring-framework/how-to-guides-spring-data-cosmosdb

@Configuration
@EnableCosmosRepositories
public class AppConfiguration extends AbstractCosmosConfiguration {

    private static final Logger logger = LoggerFactory.getLogger(AppConfiguration.class);

    @Value("${azure.cosmos.uri}")
    private String uri;

    @Value("${azure.cosmos.key}")
    private String key;

//    @Value("${azure.cosmos.secondaryKey}")
//    private String secondaryKey;

    @Value("${azure.cosmos.database}")
    private String dbName;

    @Value("${azure.cosmos.queryMetricsEnabled}")
    private boolean queryMetricsEnabled;

    private AzureKeyCredential azureKeyCredential;

    @Bean
    public CosmosClientBuilder getCosmosClientBuilder() {
        this.azureKeyCredential = new AzureKeyCredential(key);
        DirectConnectionConfig directConnectionConfig = new DirectConnectionConfig();
        GatewayConnectionConfig gatewayConnectionConfig = new GatewayConnectionConfig();
        return new CosmosClientBuilder()
                .endpoint(uri)
                .credential(azureKeyCredential)
                .directMode(directConnectionConfig, gatewayConnectionConfig);
    }

    @Override
    public CosmosConfig cosmosConfig() {
        return CosmosConfig.builder()
                .enableQueryMetrics(queryMetricsEnabled)
                .responseDiagnosticsProcessor(new ResponseDiagnosticsProcessorImplementation())
                .build();
    }

    public void switchToSecondaryKey() {
        //this.azureKeyCredential.update(secondaryKey);
    }

    @Override
    protected String getDatabaseName() {
        return "testdb";
    }

    private static class ResponseDiagnosticsProcessorImplementation implements ResponseDiagnosticsProcessor {

        @Override
        public void processResponseDiagnostics(@Nullable ResponseDiagnostics responseDiagnostics) {
            logger.info("Response Diagnostics {}", responseDiagnostics);
        }
    }

    public String getUri() {
        return uri;
    }

    public String getKey() {
        return key;
    }

//    public String getSecondaryKey() {
//        return secondaryKey;
//    }

    public String getDbName() {
        return dbName;
    }

    public boolean isQueryMetricsEnabled() {
        return queryMetricsEnabled;
    }

    public AzureKeyCredential getAzureKeyCredential() {
        return azureKeyCredential;
    }
}
