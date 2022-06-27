package org.cjoakim.cosmos.sql.rbac.processors;

//import java.util.ArrayList;
//import java.util.List;
//import java.util.Optional;
//import java.util.UUID;
//
//import com.azure.cosmos.models.PartitionKey;
//import com.fasterxml.jackson.core.JsonProcessingException;
//import org.cjoakim.cosmos.sql.rbac.data.User;
//import org.cjoakim.cosmos.sql.rbac.data.UserRepository;
//import org.slf4j.Logger;
//import org.slf4j.LoggerFactory;
//import org.springframework.beans.factory.annotation.Autowired;
//import org.springframework.boot.CommandLineRunner;
//import org.springframework.boot.SpringApplication;
//import org.springframework.boot.autoconfigure.SpringBootApplication;
//import org.springframework.context.ApplicationContext;
//

import com.azure.cosmos.models.PartitionKey;
import com.fasterxml.jackson.core.JsonProcessingException;
import lombok.NoArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.cjoakim.cosmos.sql.rbac.AppConfiguration;
import org.cjoakim.cosmos.sql.rbac.AppConstants;
import org.cjoakim.cosmos.sql.rbac.data.User;
import org.cjoakim.cosmos.sql.rbac.data.UserRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.SpringApplication;
import org.springframework.stereotype.Component;
import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.List;
import java.util.Optional;
import java.util.UUID;

@Slf4j
public class SampleUserProcessor implements MainProcessor {
    private final UserRepository repository;

    public SampleUserProcessor(final UserRepository repo) {
        this.repository = repo;
    }
    
    public void process() {
        log.warn("process...");
        log.warn("repository: " + repository);

        boolean deleteAll = AppConfiguration.booleanArg(AppConstants.DELETE_ALL);
        if (deleteAll) {
            log.warn("deleteAll starting");
            repository.deleteAll();
            log.warn("deleteAll completed");
        }

        ArrayList<User> userObjects = createUsers();

        long count = repository.countByLastName("Joakim");
        log.warn("countByLastame Joakim = " + count);

        count = repository.countByLastName("Acosta");
        log.warn("countByLastame Acosta = " + count);

        Iterable<User> userIterable = repository.findByFirstName("Miles");
        userIterable.forEach(user -> log.warn("findByFirstName: " + user));

        User userObj = userObjects.get(0);
        PartitionKey pk = new PartitionKey(userObj.getPk());
        Optional<User> userOpt = repository.findById(userObj.getId(), pk);
        if (userOpt.isPresent()) {
            User u = userOpt.get();
            log.warn("findById: present -> " + u);
            u.setFirstName("Matthew");
            repository.save(u);
        }
        else {
            log.warn("findById: not present");
        }

        log.warn("getUsersInPk ...");
        List<User> pkUsers = repository.getUsersInPk("Joakim");
        pkUsers.forEach(user -> {
            try {
                System.out.println(user.toJson());
            }
            catch (JsonProcessingException e) {
                e.printStackTrace();
            }});

        pkUsers = repository.getUsersInPk("Miles");
        pkUsers.forEach(user -> log.warn("getUsersInPk: " + user));
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
            log.warn("first: " + first + "  last: " + last + "  id: " + id);
            final User user = new User(id, first, last);
            if (i > 0) {
                user.setOther(userObjects.get(i - 1)); // turtles all the way down
            }
            log.warn("user object created: " + user);
            repository.save(user);
            log.warn("user object saved");
            userObjects.add(user);
        }
        return userObjects;
    }
}
