package org.cjoakim.cosmos.sql.spring_data_sql_gradle;

import java.util.ArrayList;
import java.util.List;
import java.util.Optional;
import java.util.UUID;

import com.azure.cosmos.models.PartitionKey;
import com.fasterxml.jackson.core.JsonProcessingException;
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

	public void run(String[] args) throws Exception {
		logger.warn("start of run() method");
		AppConfiguration.setCommandLineArgs(args);

		boolean deleteAll = AppConfiguration.booleanArg(AppConstants.DELETE_ALL);
		logger.warn("deleteAll: " + deleteAll);

		if (deleteAll) {
			logger.warn("deleteAll starting");
			repository.deleteAll();
			logger.warn("deleteAll completed");
		}

		ArrayList<User> userObjects = createUsers();

		long count = repository.countByLastName("Joakim");
		logger.warn("countByLastame Joakim = " + count);

		count = repository.countByLastName("Acosta");
		logger.warn("countByLastame Acosta = " + count);

		Iterable<User> userIterable = repository.findByFirstName("Miles");
		userIterable.forEach(user -> logger.warn("findByFirstName: " + user));

		User userObj = userObjects.get(0);
		PartitionKey pk = new PartitionKey(userObj.getPk());
		Optional<User> userOpt = repository.findById(userObj.getId(), pk);
		if (userOpt.isPresent()) {
			User u = userOpt.get();
			logger.warn("findById: present -> " + u);
			u.setFirstName("Matthew");
			repository.save(u);
		}
		else {
			logger.warn("findById: not present");
		}

		logger.warn("getUsersInPk ...");
		List<User> pkUsers = repository.getUsersInPk("Joakim");
		pkUsers.forEach(user -> {
			try {
				System.out.println(user.toJson());
			}
			catch (JsonProcessingException e) {
				e.printStackTrace();
			}});

		pkUsers = repository.getUsersInPk("Miles");
		pkUsers.forEach(user -> logger.warn("getUsersInPk: " + user));

		logger.warn("spring app exiting");
		SpringApplication.exit(this.applicationContext);
		logger.warn("spring app exit completed");
	}

	private ArrayList<User> createUsers() {

		ArrayList<String> namePairs = new ArrayList<String>();
		ArrayList<User> userObjects = new ArrayList<User>();
		namePairs.add("Chris,Joakim");
		namePairs.add("Elsa,Joakim");
		namePairs.add("Miles,Joakim");

		for (int i = 0; i < namePairs.size(); i++) {
			String[] tokens = namePairs.get(i).split(",");
			String first = tokens[0];
			String last = tokens[1];
			String id = UUID.randomUUID().toString();
			logger.warn("first: " + first + "  last: " + last + "  id: " + id);
			final User user = new User(id, first, last);
			if (i > 0) {
				user.setOther(userObjects.get(i - 1)); // turtles all the way down
			}
			logger.warn("user object created: " + user);
			repository.save(user);
			logger.warn("user object saved");
			userObjects.add(user);
		}
		return userObjects;
	}
}
