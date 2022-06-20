package org.cjoakim.cosmos.mongo.utils;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;

import com.fasterxml.jackson.core.type.TypeReference;

import java.util.HashMap;

/**
 * This class implements reusable JSON parsing and formatting logic.
 *
 * @author Chris Joakim, Microsoft
 * @date   2022/06/20
 */

public class JsonUtil {

    // Class variables:
    private static TypeReference<HashMap<String, String>> hashmapTypeRef = new TypeReference<HashMap<String, String>>() {};

    public JsonUtil() {

        super();
    }

    public Object parse(String jsonString, TypeReference ref) throws JsonProcessingException {

        ObjectMapper mapper = new ObjectMapper();
        return mapper.readValue(jsonString, ref);
    }

    public HashMap parseHashMap(String jsonString) throws JsonProcessingException {

        ObjectMapper mapper = new ObjectMapper();
        return mapper.readValue(jsonString, hashmapTypeRef);
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
