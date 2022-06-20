

# Executing this script:
# > .\execute.ps1 > tmp\execute.txt
#
# Chris Joakim, Microsoft

gradle build
gradle uberJar

$uberJar="app\build\libs\app-console-app-uber.jar"

java -jar $uberJar a b c

echo 'done'
