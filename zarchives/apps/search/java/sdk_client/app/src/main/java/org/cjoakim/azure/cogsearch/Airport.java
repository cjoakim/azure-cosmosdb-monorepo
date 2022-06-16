package org.cjoakim.azure.cogsearch;

import java.time.Instant;

import com.google.gson.JsonObject;

public class Airport {

    protected String  id;
    protected String  pk;
    protected String  name;
    protected String  city;
    protected String  country;
    protected String  iata_code;
    protected Double  latitude;
    protected Double  longitude;
    //protected Double  altitude;
    //protected Integer timezone_num;
    protected String  timezone_code;
    protected Double  epoch;
    protected String  note;

    public Airport() {
        super();
    }

    public Airport(JsonObject obj) {
        super();
        this.id = obj.get("id").getAsString();
        this.pk = obj.get("pk").getAsString();
        this.name = obj.get("name").getAsString();
        this.city = obj.get("city").getAsString();
        this.country = obj.get("country").getAsString();
        this.iata_code = obj.get("iata_code").getAsString();
        this.latitude = obj.get("latitude").getAsDouble();
        this.longitude = obj.get("longitude").getAsDouble();
        //this.altitude = obj.get("altitude").getAsDouble();
        //this.timezone_num = obj.get("timezone_num").getAsInt();
        this.timezone_code = obj.get("timezone_code").getAsString();
        Instant now = Instant.now();
        this.epoch = new Double(now.toEpochMilli());
        this.note = "loaded by java client at " + now.toString();
    }

}
