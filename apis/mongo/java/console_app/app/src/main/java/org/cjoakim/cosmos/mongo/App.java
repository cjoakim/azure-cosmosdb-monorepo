package org.cjoakim.cosmos.mongo;

import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.bson.json.JsonMode;
import org.bson.json.JsonWriterSettings;

public class App {

    // Class variables
    private static Logger logger = LogManager.getLogger(App.class);
    protected static JsonWriterSettings jsonWriterSettings =
            JsonWriterSettings.builder().indent(true).build();

    private static JsonWriterSettings jws =
            JsonWriterSettings.builder().indent(true).outputMode(JsonMode.SHELL).build();

    public static void main(String[] args) {

        if (args.length < 1) {
            logger.error("No command-line args; terminating...");
        }
        else {
            try {
                AppConfig.setCommandLineArgs(args);
                String function = args[0];

                switch (function) {
                    case "loadContainerFromCsv":
                        loadContainerFromCsv(args);
                        break;
                    case "truncateContainer":
                        truncateContainer(args);
                        break;
                    default:
                        logger.error("unknown main function: " + function);
                }
            }
            catch (Exception e) {
                e.printStackTrace();
            }
        }
    }

    private static void loadContainerFromCsv(String[] args) {

        try {
            String connStringEnvVarName = args[1];
            String dbName  = args[2];
            String cName   = args[3];
            String csvFile = args[4];
            String connStr = AppConfig.getEnvVar(connStringEnvVarName);

            logger.warn("envVarName: " + connStringEnvVarName);
            logger.warn("connString: " + connStr);
            logger.warn("dbName:     " + dbName);
            logger.warn("cName:      " + cName);
            logger.warn("csvFile:    " + csvFile);

            MongoUtil mu = new MongoUtil(connStr);
            mu.setCurrentDatabase(dbName);
            mu.setCurrentCollection(cName);

            // TODO - implement
        }
        catch (Exception e) {
            throw new RuntimeException(e);
        }
    }


    private static void truncateContainer(String[] args) {

        try {
            String connStringEnvVarName = args[1];
            String dbName = args[2];
            String cName = args[3];
            String connStr = AppConfig.getEnvVar(connStringEnvVarName);

            logger.warn("envVarName: " + connStringEnvVarName);
            logger.warn("connString: " + connStr);
            logger.warn("dbName:     " + dbName);
            logger.warn("cName:      " + cName);

            MongoUtil mu = new MongoUtil(connStr);
            mu.setCurrentDatabase(dbName);
            mu.setCurrentCollection(cName);

            // TODO - implement
        }
        catch (Exception e) {
            throw new RuntimeException(e);
        }
    }

}
