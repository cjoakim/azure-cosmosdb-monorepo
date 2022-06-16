package org.cjoakim.azure.changefeed;

/**
 * This interface defines constant values used in this application.
 * These include the names of environment variables.
 * 
 * @author Chris Joakim, Microsoft
 * @date   2021/03/19
 */
public interface AppConstants {

	// Environment variables (these are my conventions, not Microsoft's)
	public static final String AZURE_COSMOSDB_SQLDB_DBNAME   = "AZURE_COSMOSDB_SQLDB_DBNAME";
	public static final String AZURE_COSMOSDB_SQLDB_COLLNAME = "AZURE_COSMOSDB_SQLDB_COLLNAME";
	public static final String AZURE_COSMOSDB_SQLDB_KEY      = "AZURE_COSMOSDB_SQLDB_KEY";
	public static final String AZURE_COSMOSDB_SQLDB_URI      = "AZURE_COSMOSDB_SQLDB_URI";

	public static final long   MS_PER_MINUTE                 = 1000 * 60; 
	public static final long   MS_PER_HOUR                   = 1000 * 60 * 60; 
}
