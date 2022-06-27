package org.cjoakim.cosmos.sql.rbac.processors;

import com.fasterxml.jackson.databind.ObjectMapper;
import lombok.extern.slf4j.Slf4j;
import org.cjoakim.cosmos.sql.rbac.data.AzureRole;
import org.cjoakim.cosmos.sql.rbac.data.AzureRoleRepository;

import java.io.File;
import java.io.FileNotFoundException;
import java.nio.file.Paths;
import java.util.Map;
import java.util.Scanner;

@Slf4j
public class RbacLoader implements MainProcessor {

    private AzureRoleRepository azureRoleRepository;
    public void process() {
        log.warn("process...");

        loadAzureRoles();
    }

    private void loadAzureRoles() {

        log.warn("loadAzureRoles...");
        ObjectMapper mapper = new ObjectMapper();
        String filename = "data/azure_roles.json";
        File f = new File(filename);
        if (f.exists()) {
            log.warn("exists: " + filename);
            try {
                Scanner sc = new Scanner(f);
                while (sc.hasNextLine()) {
                    String line = sc.nextLine().trim();
                    System.out.println(line);

                    AzureRole obj = mapper.readValue(line, AzureRole.class);
                    System.out.println(obj);
                }
            }
            catch (Exception e) {
                throw new RuntimeException(e);
            }
        }
        else {
            log.warn("file does not exist: " + filename);
        }
    }
}
