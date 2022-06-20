package org.cjoakim.cosmos.mongo.utils;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;

import com.fasterxml.jackson.core.type.TypeReference;

import java.io.IOException;

//import com.fasterxml.jackson.core.JsonParseException;
//import com.fasterxml.jackson.core.type.TypeReference;
//import com.fasterxml.jackson.databind.JsonMappingException;
//import com.fasterxml.jackson.databind.ObjectMapper;


/**
 * This class implements reusable JSON parsing and formatting logic.
 *
 * @author Chris Joakim, Microsoft
 * @date   2022/06/20
 */

public class JsonUtil {

    public JsonUtil() {

        super();
    }

    public Object parse(String jsonString, TypeReference ref) throws Exception {

        ObjectMapper mapper = new ObjectMapper();
        return mapper.readValue(jsonString, ref);
    }

    public String pretty(Object obj) {

        ObjectMapper mapper = new ObjectMapper();
        try {
            return mapper.writerWithDefaultPrettyPrinter().writeValueAsString(obj);
        }
        catch (JsonProcessingException e) {
            e.printStackTrace();
            return null;
        }
    }
}
