package org.cjoakim.azure.changefeed;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.core.env.Environment;
import org.springframework.stereotype.Component;

/**
 * This class leverages Spring Boot functionality to read configuration values
 * from application.properties, command-line args, and environment variables.
 * 
 * @author Chris Joakim, Microsoft
 * @date   2021/03/19
 */

@Component
public class AppConfig implements AppConstants {

    @Autowired
    private Environment env;
    
	@Value("${app.name}")
    private String appName;
	
	//
	
	@Value("${AZURE_COSMOSDB_SQLDB_URI:}")
	private String cosmosSqlUri;
	
	@Value("${AZURE_COSMOSDB_SQLDB_KEY:}")
	private String cosmosSqlKey;
	
	@Value("${AZURE_COSMOSDB_SQLDB_DBNAME:}")
	private String cosmosSqlDbname;
	
	@Value("${AZURE_COSMOSDB_SQLDB_COLLNAME:}")
	private String cosmosSqlCollname;
	
	@Value("${AZURE_COSMOSDB_SQLDB_COLLNAME:}")
	private String cosmosSqlContainer;  // alias for the above; "collection" and "container" are synonymous
	
	//
	
	public String getAppName() {
		return appName;
	}

	public void setAppName(String appName) {
		this.appName = appName;
	}

	public String getCosmosSqlUri() {
		return cosmosSqlUri;
	}

	public void setCosmosSqlUri(String cosmosSqlUri) {
		this.cosmosSqlUri = cosmosSqlUri;
	}

	public String getCosmosSqlKey() {
		return cosmosSqlKey;
	}

	public void setCosmosSqlKey(String cosmosSqlKey) {
		this.cosmosSqlKey = cosmosSqlKey;
	}

	public String getCosmosSqlDbname() {
		return cosmosSqlDbname;
	}

	public void setCosmosSqlDbname(String cosmosSqlDbname) {
		this.cosmosSqlDbname = cosmosSqlDbname;
	}

	public String getCosmosSqlCollname() {
		return cosmosSqlCollname;
	}

	public void setCosmosSqlCollname(String cosmosSqlCollname) {
		this.cosmosSqlCollname = cosmosSqlCollname;
	}

	public String getCosmosSqlContainer() {
		return cosmosSqlContainer;
	}

	public void setCosmosSqlContainer(String cosmosSqlContainer) {
		this.cosmosSqlContainer = cosmosSqlContainer;
	}

	public String getEnvVar(String name, String defaultValue) {
		
		String value = null;
		try {
			value = env.getProperty(name);
			if (value == null) {
				value = defaultValue;
			}
		}
		catch (Exception e) {
			value = defaultValue;
		}
		return value;
	}
}

