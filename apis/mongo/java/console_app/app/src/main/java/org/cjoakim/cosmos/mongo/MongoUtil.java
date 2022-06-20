package org.cjoakim.cosmos.mongo;

import com.mongodb.ConnectionString;
import com.mongodb.MongoClientSettings;
import com.mongodb.ServerApi;
import com.mongodb.ServerApiVersion;
import com.mongodb.client.*;
import com.mongodb.client.model.Filters;
import com.mongodb.client.model.IndexModel;
import com.mongodb.client.model.ReplaceOptions;
import com.mongodb.client.result.DeleteResult;
import com.mongodb.client.result.InsertOneResult;
import com.mongodb.client.result.UpdateResult;
import com.mongodb.client.model.Indexes;
import com.mongodb.client.model.IndexOptions;

import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.bson.BsonDocument;
import org.bson.Document;
import org.bson.codecs.configuration.CodecRegistry;
import org.bson.conversions.Bson;
import org.bson.json.JsonWriterSettings;
import org.bson.types.ObjectId;

import static com.mongodb.client.model.Filters.eq;

import java.util.*;

/**
 * This class implements MongoDB database operations, including the CosmosDB/Mongo API.
 * Chris Joakim, Microsoft
 */

public class MongoUtil {

    // Class variables
    private static Logger logger = LogManager.getLogger(MongoUtil.class);

    // Instance variables:
    protected MongoClient mongoClient;
    protected MongoDatabase currentDatabase;
    protected MongoCollection<Document> currentCollection;
    protected String currentShardKey;
    protected JsonWriterSettings jsonWriterSettings;


    public MongoUtil(String connStr) throws Exception {

        super();
        ConnectionString connectionString = new ConnectionString(connStr);
        MongoClientSettings settings = MongoClientSettings.builder()
                .applicationName("ts")
                .applyConnectionString(connectionString)
                .build();

        logger.warn("MongoClientSettings, app name: " + settings.getApplicationName());
        mongoClient = MongoClients.create(settings);

        if (mongoClient == null) {
            logger.error("MongoClients.create returned null object");
        }
        else {
            logger.warn("MongoClients.create " + mongoClient.getClusterDescription());
        }
        setJsonWriterSettings(true);
    }

    public MongoClient getMongoClient() {

        return mongoClient;
    }

    public MongoDatabase getCurrentDatabase() {

        return currentDatabase;
    }

    public void setCurrentDatabase(String name) {

        this.currentDatabase = mongoClient.getDatabase(name);
    }

    public MongoCollection<Document> getCurrentCollection() {

        return currentCollection;
    }

    public void setCurrentCollection(String name) {

        this.currentCollection = this.currentDatabase.getCollection(name);
    }

    public String getCurrentShardKey() {

        return currentShardKey;
    }

    public void setShardKey(String name) {

        this.currentShardKey = name;
    }

    public JsonWriterSettings getJsonWriterSettings() {

        return jsonWriterSettings;
    }

    public void setJsonWriterSettings(boolean pretty) {

        jsonWriterSettings = JsonWriterSettings.builder().indent(pretty).build();
    }

    public InsertOneResult insertDoc(HashMap map) {

        return this.insertDoc(new Document(map));
    }

    public InsertOneResult insertDoc(Document doc) {

        return this.currentCollection.insertOne(doc);
    }

    public UpdateResult replaceOne(Document doc) throws Exception {

        // https://www.mongodb.com/docs/drivers/java/sync/current/usage-examples/replaceOne/
        ObjectId id = (ObjectId) doc.get("_id");
        Bson query = eq("_id", id);
        logger.warn("replaceOne query: " + query.toBsonDocument());
        ReplaceOptions opts = new ReplaceOptions().upsert(true);
        return this.currentCollection.replaceOne(query, doc, opts);
    }

    public DeleteResult deleteOne(Document doc) throws Exception {

        ObjectId id = (ObjectId) doc.get("_id");
        Bson query = eq("_id", id);
        logger.warn("deleteOne query: " + query.toBsonDocument());
        return this.currentCollection.deleteOne(query);
    }

    public FindIterable<Document> find() {

        return this.currentCollection.find();
    }

    public Document findOne() {

        return this.currentCollection.find().first();
    }

    public FindIterable<Document> findByPk(String pk, boolean explain) {

        Bson pkFilter = eq("pk", pk);

        if (explain) {
            Document doc = this.currentCollection.find(pkFilter).explain();
            logger.warn("findByPk explain: " + doc.toJson(jsonWriterSettings));
        }
        return this.currentCollection.find(pkFilter);
    }

    public Document findByIdPk(String id, String pk, boolean explain) {

        Bson idFilter = eq("_id", id);
        Bson pkFilter = eq("pk", pk);

        if (explain) {
            Document doc = this.currentCollection.find(Filters.and(idFilter, pkFilter)).explain();
            logger.warn("findByIdPk explain: " + doc.toJson(jsonWriterSettings));
        }
        return this.currentCollection.find(Filters.and(idFilter, pkFilter)).first();
    }

    /**
     * This method applies only to CosmosDB, not MongoDB.
     * See https://docs.microsoft.com/en-us/azure/cosmos-db/mongodb/find-request-unit-charge-mongodb#use-the-mongodb-java-driver
     */
    public Document getLastRequestStatistics() {

        return this.currentDatabase.runCommand(new Document("getLastRequestStatistics", 1));
    }

    /**
     * This method applies only to CosmosDB, not MongoDB.
     */
    public double getLastRequestCharge() {

        Document stats = this.getLastRequestStatistics();
        if (stats != null) {
            return stats.getDouble("RequestCharge");
        }
        else {
            return -1.0;
        }
    }

    public String createIndex(ArrayList<Object> indexes, boolean unique) {
        Bson index = null;
        if (indexes.toArray().length == 1) // Single field index
        {
            String key = (String) ((ArrayList<Object>) indexes.toArray()[0]).toArray()[0];
            Integer direction = (Integer) ((ArrayList<Object>) indexes.toArray()[0]).toArray()[1];

            //Object key, Integer direction

            if (!unique) {
                index = (direction == 1) ? Indexes.ascending((String) key) : Indexes.descending((String) key);
                return this.currentCollection.createIndex(index);
            } else {
                index = (direction == 1) ? Indexes.compoundIndex(Indexes.ascending(this.currentShardKey), Indexes.ascending((String) key)) : Indexes.compoundIndex(Indexes.ascending(this.currentShardKey), Indexes.descending((String) key));
                return this.currentCollection.createIndex(index, new IndexOptions().unique(unique));
            }
        }
        else
        {
            List<Bson> compoundIndex = new ArrayList<Bson>();
            for (int i = 0; i < indexes.toArray().length; i++)
            {
                if (i == 0)
                    continue;

                if (i == 1) {
                    String firstKey = (String) ((ArrayList<Object>) indexes.toArray()[0]).toArray()[0];
                    Double firstDirection = (Double) ((ArrayList<Object>) indexes.toArray()[0]).toArray()[1];
                    compoundIndex.add((firstDirection == 1.0) ? Indexes.ascending(firstKey) : Indexes.descending(firstKey));

                    String secondKey = (String) ((ArrayList<Object>) indexes.toArray()[1]).toArray()[0];
                    Double secondDirection = (Double) ((ArrayList<Object>) indexes.toArray()[1]).toArray()[1];
                    compoundIndex.add((secondDirection == 1.0) ? Indexes.ascending(secondKey) : Indexes.descending(secondKey));
                }
                else
                {
                    String key = (String) ((ArrayList<Object>) indexes.toArray()[i]).toArray()[0];
                    Double direction = (Double) ((ArrayList<Object>) indexes.toArray()[i]).toArray()[1];

                    compoundIndex.add((direction == 1.0) ? Indexes.ascending(key) : Indexes.descending(key));
                }
            }

            index = Indexes.compoundIndex(compoundIndex);

            return this.currentCollection.createIndex(index, new IndexOptions().unique(unique));
        }
    }

}
