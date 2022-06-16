#!/bin/bash

# Compile the application with the Gradle build tool.
# Chris Joakim, Microsoft, December 2021

./gradlew runApp --args="search airports All"

./gradlew runApp --args="search airports CLT"

./gradlew runApp --args="search airports Charlotte"
