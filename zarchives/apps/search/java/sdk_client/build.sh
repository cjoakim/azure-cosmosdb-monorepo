#!/bin/bash

# Compile the application with the Gradle build tool.
# Chris Joakim, Microsoft, December 2021

#./gradlew app:dependencies --configuration runtimeClasspathh

./gradlew app:dependencies --configuration implementation

./gradlew app:build


# gradle distZip --exclude-task test
#   creates app/build/distributions/app.zip

# ./gradlew runConsumer --warning-mode all

