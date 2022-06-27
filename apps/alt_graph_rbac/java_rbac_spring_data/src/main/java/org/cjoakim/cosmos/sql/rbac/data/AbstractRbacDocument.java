package org.cjoakim.cosmos.sql.rbac.data;

import com.azure.spring.data.cosmos.core.mapping.Container;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.extern.slf4j.Slf4j;

@Container(containerName = "rbac")
@NoArgsConstructor
@AllArgsConstructor
@Data
@Slf4j
public abstract class AbstractRbacDocument {

    private String id;
    private String pk;
    private String doctype;
}
