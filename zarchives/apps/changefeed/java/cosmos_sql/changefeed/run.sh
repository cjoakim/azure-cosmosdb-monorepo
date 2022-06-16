#!/bin/bash

# Executes this Spring Boot app.
# Chris Joakim, 2021/03/19

./build.sh

jar="target/changefeed-0.0.1.jar"
main_functions="consume"

java -Xmx200m \
    -Ddebug=true \
    -Dspring.profiles.active=default \
    -jar $jar $main_functions
