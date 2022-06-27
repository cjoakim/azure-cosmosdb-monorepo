package org.cjoakim.cosmos.sql.rbac.data;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.extern.slf4j.Slf4j;

@NoArgsConstructor
@AllArgsConstructor
@Data
@Slf4j
public class AzureRole extends AbstractRbacDocument {

    private String role;
    private String href;
    private String desc;
}
