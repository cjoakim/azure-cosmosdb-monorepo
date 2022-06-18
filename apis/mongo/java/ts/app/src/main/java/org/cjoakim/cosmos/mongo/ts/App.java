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
import static com.mongodb.client.model.Filters.exists;

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
                    case "addTimestamp":
                        addTimestamp(args);
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

    private static void addTimestamp(String[] args) {

        try {
            String  connStringEnvVarName = args[1];
            String  dbName   = args[2];
            String  cName    = args[3];
            String  connStr  = AppConfig.getEnvVar(connStringEnvVarName);
            boolean explain  = AppConfig.booleanArg("--explain");
            boolean update   = AppConfig.booleanArg("--update");

            logger.warn("envVarName: " + connStringEnvVarName);
            logger.warn("connString: " + connStr);
            logger.warn("dbName:     " + dbName);
            logger.warn("cName:      " + cName);
            logger.warn("explain:    " + explain);
            logger.warn("update:     " + update);

            MongoUtil mu = new MongoUtil(connStr);
            mu.setCurrentDatabase(dbName);
            mu.setCurrentCollection(cName);

            long count = mu.getCurrentCollection().countDocuments();
            logger.warn("document count in collection: " + count);

            String ttlAttributeName = "_ts";  // should be _ts

            // Create the Filter
            Bson stateNyFilter = eq("state", "NY");
            Bson notExistsFilter = exists(ttlAttributeName, false);
            Bson filter = notExistsFilter;

            // dev> db.baseball_core_Parks.find({state: "MA"})
            // dev> db.baseball_core_Parks.find({"city": "Boston"})

            if (explain) {
                Document xdoc = mu.currentCollection.find(filter).explain();
                logger.warn("find explain: " + xdoc.toJson(jsonWriterSettings));
            }
            FindIterable<Document> findIterable = mu.getCurrentCollection().find(filter);
            MongoCursor<Document> cursor = findIterable.iterator();
            long docsFoundCount = 0;
            long docsUpdatedCount = 0;

            while (cursor.hasNext()) {
                docsFoundCount++;
                System.out.println("=== " + docsFoundCount);
                Document doc = cursor.next();
                System.out.println(doc.toJson(jsonWriterSettings));
                System.out.println("-");

                // Implement your _ts value logic here:
                doc.put(ttlAttributeName, (long) (System.currentTimeMillis() / 1000));  // default value
                String parkName = (String) doc.get("park.name");
                System.out.println("park.name: " + parkName);

                if (parkName.equalsIgnoreCase("Fenway Park")) {
                    System.out.println("'Fenway Park' is eternal");
                    doc.put(ttlAttributeName, Long.MAX_VALUE);
                }
                if (parkName.equalsIgnoreCase("Hartford Ball Club Grounds")) {
                    System.out.println("'Hartford Ball Club Grounds' can be expired in an hour");
                    doc.put(ttlAttributeName, 3600);
                }

                // Display the updated document (before optionally updating it)
                System.out.println(doc.toJson());

                if (update) {
                    UpdateResult result = mu.replaceOne(doc);
                    long modCount = result.getModifiedCount();
                    docsUpdatedCount = docsUpdatedCount + modCount;
                    System.out.println("Modified document count: " + modCount +  ", total: " + docsUpdatedCount);
                }
                else {
                    System.out.println("update bypassed per CLI arg");
                }
            }
            logger.warn("documents found count:   " + docsFoundCount);
            logger.warn("documents updated count: " + docsUpdatedCount);
        }
        catch (Exception e) {
            throw new RuntimeException(e);
        }
    }
}

/**

The documents in the 'baseball_core_Parks' collection look like this:

 {
 "_id": {
 "$oid": "62812a502dbef1cfff7ebbf7"
 },
 "idx": 246,
 "park.key": "WAT01",
 "park.name": "Troy Ball Club Grounds",
 "park.alias": "",
 "city": "Watervliet",
 "state": "NY",
 "country": "US",
 "doctype": "core_Parks",
 "notes": [
 "Both great next receive. Respond region heart traditional measure sea.",
 "Animal light minute control. Public involve suggest effort war small. Along music baby let music maybe experience matter. Game somebody pull gun at.",
 "Reveal subject central coach guy thing. Full serve raise garden effect parent contain. Front whole staff go section stock particular.",
 "Leave theory lawyer camera environment together. Wish woman so while effect term also.",
 "Machine dog woman she. Begin on energy for can tend president. Never painting baby get."
 ],
 "source_data_attribution": "https://www.seanlahman.com/baseball-archive/statistics/",
 "_asz": 855,
 "_generated_at": "2022-05-15T16:29:04.871031+00:00"
 }

 */
