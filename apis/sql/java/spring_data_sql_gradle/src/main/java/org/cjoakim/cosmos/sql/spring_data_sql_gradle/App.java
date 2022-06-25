package org.cjoakim.cosmos.sql.spring_data_sql_gradle;

import java.util.ArrayList;
import java.util.UUID;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.CommandLineRunner;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.ApplicationContext;

@SpringBootApplication
public class App implements CommandLineRunner, AppConstants {

	private static final Logger logger = LoggerFactory.getLogger(App.class);

	@Autowired
	private UserRepository repository;

	@Autowired
	private ApplicationContext applicationContext;

	@Autowired
	private AppConfiguration appConfiguration;

	public static void main(String[] args) {
		SpringApplication.run(App.class, args);
	}

	public void run(String[] args) {
		logger.warn("start of run() method");
		AppConfiguration.setCommandLineArgs(args);

		boolean deleteAll = AppConfiguration.booleanArg(AppConstants.DELETE_ALL);
		logger.warn("deleteAll: " + deleteAll);

		if (deleteAll) {
			logger.warn("deleteAll starting");
			repository.deleteAll();
			logger.warn("deleteAll completed");
		}

		createUsers();

		logger.warn("spring app exiting");
		SpringApplication.exit(this.applicationContext);
		logger.warn("spring app exit completed");
	}

	private void createUsers() {

		ArrayList<String> namePairs = new ArrayList<String>();
		namePairs.add("Chris,Joakim");
		namePairs.add("Elsa,Joakim");
		namePairs.add("Miles,Joakim");

		for (int i = 0; i < namePairs.size(); i++) {
			String[] tokens = namePairs.get(i).split(",");
			String first = tokens[0];
			String last  = tokens[1];
			String id = UUID.randomUUID().toString();
			logger.warn("first: " + first + "  last: " + last + "  id: " + id);
			final User user = new User(id, first, last);
			logger.warn("user object created: " + user);
			repository.save(user);
			logger.warn("user object saved");
		}
	}
}
