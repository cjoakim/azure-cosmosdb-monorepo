package org.cjoakim.cosmos.mongo.ts;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.mongodb.BasicDBObject;
import com.mongodb.client.FindIterable;
import com.mongodb.client.MongoCursor;
import com.mongodb.client.model.UpdateOptions;
import com.mongodb.client.model.Updates;
import com.mongodb.client.result.DeleteResult;
import com.mongodb.client.result.UpdateResult;
import org.bson.Document;
import org.bson.conversions.Bson;
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

import static com.mongodb.client.model.Filters.eq;

public class App {

    // Class variables
    private static Logger logger = LogManager.getLogger(App.class);

    protected static JsonWriterSettings jsonWriterSettings =
            JsonWriterSettings.builder().indent(true).build();

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
            Bson filter = eq("country", "US");

            if (false) {
                Document explain = mu.currentCollection.find(filter).explain();
                logger.warn("find explain: " + explain.toJson(jsonWriterSettings));
            }
            FindIterable<Document> findIterable = mu.getCurrentCollection().find(filter);
            MongoCursor<Document> cursor = findIterable.iterator();

            if (cursor.hasNext()) {
                Document doc = cursor.next();
                logger.warn(doc.toJson());
                doc.put("updated_at", System.currentTimeMillis());
                logger.warn(doc.toJson());

                Bson updates = Updates.combine(
                        Updates.set("updated_at", System.currentTimeMillis()));
                UpdateOptions options = new UpdateOptions().upsert(false);
                UpdateResult result = mu.getCurrentCollection().updateOne(
                        doc.toBsonDocument(), updates, options);
                logger.warn("Modified document count: " + result.getModifiedCount());

            }

        }
        catch (Exception e) {
            throw new RuntimeException(e);
        }
    }
}
