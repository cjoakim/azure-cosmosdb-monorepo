#!/bin/bash

# Builds this Spring Boot app; creates an "uber jar".
# Chris Joakim, 2021/03/19

rm target/changefeed-0.0.1.jar

mvn clean compile package -Dmaven.test.skip=true

# jar tvf target/changefeed-0.0.1.jar
