package org.cjoakim.cosmos.sql.rbac;

import java.util.ArrayList;
import java.util.List;
import java.util.Optional;
import java.util.UUID;

import com.azure.cosmos.models.PartitionKey;
import com.fasterxml.jackson.core.JsonProcessingException;
import lombok.extern.slf4j.Slf4j;
import org.cjoakim.cosmos.sql.rbac.data.User;
import org.cjoakim.cosmos.sql.rbac.data.UserRepository;
import org.cjoakim.cosmos.sql.rbac.processors.MainProcessor;
import org.cjoakim.cosmos.sql.rbac.processors.SampleUserProcessor;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.CommandLineRunner;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.ApplicationContext;

@SpringBootApplication
@Slf4j
public class App implements CommandLineRunner, AppConstants {

	@Autowired
	private UserRepository userRepository;

	@Autowired
	private ApplicationContext applicationContext;

	@Autowired
	private AppConfiguration appConfiguration;

	public static void main(String[] args) {
		SpringApplication.run(App.class, args);
	}

	/**
	 * This is effectively the entry-point for a Spring Boot application,
	 * called from the above main method.  Create and invoke a MainProcessor
	 * instance based on CLI args.
	 */
	public void run(String[] args) throws Exception {
		AppConfiguration.setCommandLineArgs(args);
		String process = args[0];
		log.warn("process: " + process);

		try {
			switch (process) {
				case "sample_users":
					MainProcessor processor = new SampleUserProcessor(userRepository);
					processor.process();
					break;
				default:
					log.error("unknown CLI process name: " + process);
			}
		}
		catch (Exception e) {
			throw new RuntimeException(e);
		}
		finally {
			log.warn("spring app exiting");
			SpringApplication.exit(this.applicationContext);
			log.warn("spring app exit completed");
		}
	}
}
