package org.cjoakim.cosmos.mongo.ts;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.mongodb.client.FindIterable;
import com.mongodb.client.MongoCursor;
import com.mongodb.client.result.DeleteResult;
import org.bson.Document;
import org.bson.json.JsonMode;
import org.bson.json.JsonWriterSettings;
import org.bson.types.ObjectId;

import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;

import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.Paths;
import java.text.SimpleDateFormat;
import java.util.*;

public class App {

    // Class variables
    private static Logger logger = LogManager.getLogger(App.class);

    private static JsonWriterSettings jws =
            JsonWriterSettings.builder().indent(true).outputMode(JsonMode.SHELL).build();

    public String getGreeting() {
        return "Hello World!";
    }

    public static void main(String[] args) {

        if (args.length < 1) {
            logger.error("No command-line args; terminating...");
        }
        else {
            try {
                AppConfig.setCommandLineArgs(args);
                String function = args[0];

                switch (function) {
                    case "connectTest":
                        connectTest(args);
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

    private static void connectTest(String[] args) {
        // args 'connectTest', 'AZURE_ATLAS_CONN_STR', 'dev', 'baseball_core_Parks'
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

            long count = mu.getCurrentCollection().countDocuments();
            logger.warn("document count: " + count);


        }
        catch (Exception e) {
            throw new RuntimeException(e);
        }
    }
}
