
# Get the Java CLASSPATH from Gradle, redirect it to a tmp/ file.
# Chris Joakim, Microsoft, June 2022

gradle dependencies --configuration runtimeClasspath > tmp\gradle_classpath.txt
