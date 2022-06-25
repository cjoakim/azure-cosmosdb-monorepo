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

@Configuration
@EnableCosmosRepositories
public class AppConfiguration extends AbstractCosmosConfiguration
        implements AppConstants {

    private static final Logger logger = LoggerFactory.getLogger(AppConfiguration.class);
    private static String[] commandLineArgs = null;

    protected static void setCommandLineArgs(String[] args) {
        commandLineArgs = args;
        if (commandLineArgs == null) {
            logger.warn("setCommandLineArgs; null");
        }
        else {
            logger.warn("setCommandLineArgs; length: " + commandLineArgs.length);
            for (int i = 0; i < commandLineArgs.length; i++) {
                logger.warn("setCommandLineArgs, idx: " + i + " -> " + commandLineArgs[i]);
            }
        }
    }

    public static String flagArg(String flagArg) {

        for (int i = 0; i < commandLineArgs.length; i++) {
            if (commandLineArgs[i].equalsIgnoreCase(flagArg)) {
                return commandLineArgs[i + 1];
            }
        }
        return null;
    }

    public static boolean booleanArg(String flagArg) {

        for (int i = 0; i < commandLineArgs.length; i++) {
            if (commandLineArgs[i].equalsIgnoreCase(flagArg)) {
                return true;
            }
        }
        return false;
    }

    public static long longFlagArg(String flagArg, long defaultValue) {

        try {
            return Long.parseLong(flagArg(flagArg));
        }
        catch (NumberFormatException e) {
            return defaultValue;
        }
    }

    public static boolean isVerbose() {

        return booleanArg(VERBOSE_FLAG);
    }

    public static boolean isSilent() {

        return booleanArg(SILENT_FLAG);
    }

    public static boolean isPretty() {

        return booleanArg(PRETTY_FLAG);
    }



    //@Value("${azure.cosmos.uri}")
    @Value("${spring.cloud.azure.cosmos.endpoint}")
    private String uri;

    //@Value("${azure.cosmos.key}")
    @Value("${spring.cloud.azure.cosmos.key}")
    private String key;

    @Value("${azure.cosmos.secondaryKey}")
    private String secondaryKey;

    //@Value("${azure.cosmos.database}")
    @Value("${spring.cloud.azure.cosmos.database}")
    private String dbName;

    @Value("${azure.cosmos.queryMetricsEnabled}")
    private boolean queryMetricsEnabled;

    @Value("${azure.cosmos.maxDegreeOfParallelism}")
    private int maxDegreeOfParallelism;

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
                //.maxDegreeOfParallelism(maxDegreeOfParallelism)
                .responseDiagnosticsProcessor(new ResponseDiagnosticsProcessorImplementation())
                .build();
    }

    public void switchToSecondaryKey() {
        this.azureKeyCredential.update(secondaryKey);
    }

    @Override
    protected String getDatabaseName() {
        return "dev";
    }

    private static class ResponseDiagnosticsProcessorImplementation implements ResponseDiagnosticsProcessor {

        @Override
        public void processResponseDiagnostics(@Nullable ResponseDiagnostics responseDiagnostics) {
            logger.info("Response Diagnostics {}", responseDiagnostics);
        }
    }

}