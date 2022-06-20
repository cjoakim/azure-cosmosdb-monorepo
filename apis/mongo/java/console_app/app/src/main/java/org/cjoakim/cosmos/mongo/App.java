package org.cjoakim.cosmos.mongo;

import com.fasterxml.jackson.core.type.TypeReference;
import com.mongodb.client.FindIterable;
import com.mongodb.client.MongoCursor;
import com.mongodb.client.model.Filters;
import com.mongodb.client.result.DeleteResult;
import com.mongodb.client.result.InsertOneResult;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.bson.Document;
import org.bson.conversions.Bson;
import org.bson.json.JsonMode;
import org.bson.json.JsonWriterSettings;
import org.cjoakim.cosmos.mongo.utils.JsonUtil;

import java.io.File;
import java.util.HashMap;
import java.util.Map;
import java.util.Scanner;

import static com.mongodb.client.model.Filters.eq;
import static com.mongodb.client.model.Filters.exists;

/**
 * This is the entry-point class for this application, see the main() method.
 *
 * @author Chris Joakim, Microsoft
 * @date   2022/06/20
 */

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
                    case "queryContainer":
                        queryContainer(args);
                        break;
                    case "loadContainerFromJson":
                        loadContainerFromJson(args);
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

    private static void queryContainer(String[] args) {

        try {
            String connStringEnvVarName = args[1];
            String dbName  = args[2];
            String cName   = args[3];
            String connStr = AppConfig.getEnvVar(connStringEnvVarName);

            logger.warn("envVarName: " + connStringEnvVarName);
            logger.warn("connString: " + connStr);
            logger.warn("dbName:     " + dbName);
            logger.warn("cName:      " + cName);

            MongoUtil mu = new MongoUtil(connStr);
            mu.setCurrentDatabase(dbName);
            mu.setCurrentCollection(cName);

            String ttlAttributeName = "_ts";

            // Create the Filter
            Bson filter = Filters.empty();

            FindIterable<Document> findIterable = mu.getCurrentCollection().find(filter);
            MongoCursor<Document> cursor = findIterable.iterator();
            long docsFoundCount = 0;
            long docsUpdatedCount = 0;

            while (cursor.hasNext()) {
                docsFoundCount++;
                System.out.println("=== " + docsFoundCount);
                Document doc = cursor.next();
                System.out.println(doc.toJson(jsonWriterSettings));
            }
        }
        catch (Exception e) {
            throw new RuntimeException(e);
        }
    }

    private static void loadContainerFromJson(String[] args) {

        try {
            String connStringEnvVarName = args[1];
            String dbName  = args[2];
            String cName   = args[3];
            String infile  = args[4];
            String connStr = AppConfig.getEnvVar(connStringEnvVarName);

            logger.warn("envVarName: " + connStringEnvVarName);
            logger.warn("connString: " + connStr);
            logger.warn("dbName:     " + dbName);
            logger.warn("cName:      " + cName);
            logger.warn("infile:     " + infile);

            MongoUtil mu = new MongoUtil(connStr);
            mu.setCurrentDatabase(dbName);
            mu.setCurrentCollection(cName);

            JsonUtil jsonUtil = new JsonUtil();
            long linesReadCount = 0;
            long docsWrittenCount = 0;

            Scanner scanner = new Scanner(new File(infile));
            while (scanner.hasNextLine()) {
                String line = scanner.nextLine();
                linesReadCount++;
                HashMap map = (HashMap) jsonUtil.parseHashMap(line.trim());
                logger.warn(map);
                InsertOneResult result = mu.insertDoc(map);
                String id = result.getInsertedId().toString();
                if (id  != null) {
                    docsWrittenCount++;
                }
            }
            logger.warn("lines read:   " + linesReadCount);
            logger.warn("docs written: " + docsWrittenCount);
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
            boolean verbose = AppConfig.booleanArg("--verbose");

            logger.warn("envVarName: " + connStringEnvVarName);
            logger.warn("connString: " + connStr);
            logger.warn("dbName:     " + dbName);
            logger.warn("cName:      " + cName);

            MongoUtil mu = new MongoUtil(connStr);
            mu.setCurrentDatabase(dbName);
            mu.setCurrentCollection(cName);
            boolean continueToProcess = true;
            long findLoopCounter  = 0;
            long docsFoundCount   = 0;
            long docsDeletedCount = 0;
            Bson filter = Filters.empty();

            while (continueToProcess) {
                findLoopCounter++;
                FindIterable<Document> findIterable = mu.getCurrentCollection().find(filter);
                MongoCursor<Document> cursor = findIterable.iterator();
                long loopDocsFoundCount = 0;
                while (cursor.hasNext()) {
                    docsFoundCount++;
                    loopDocsFoundCount++;
                    Document doc = cursor.next();
                    if (verbose) {
                        System.out.println("=== find loop: " + findLoopCounter + ", doc: " + docsFoundCount);
                        System.out.println(doc.toJson(jsonWriterSettings));
                    }
                    DeleteResult result = mu.deleteOne(doc);
                    docsDeletedCount = docsDeletedCount + result.getDeletedCount();
                }
                if (cursor != null) {
                    cursor.close();
                }
                if (loopDocsFoundCount < 1) {
                    continueToProcess = false;
                    logger.warn("exiting find loop; no more documents found");
                }
                if (findLoopCounter > 10000) {
                    continueToProcess = false;
                    logger.warn("exiting find loop; runaway loop");
                }
            }
            logger.warn("docs found:   " + docsFoundCount);
            logger.warn("docs deleted: " + docsDeletedCount);
        }
        catch (Exception e) {
            throw new RuntimeException(e);
        }
    }

}
