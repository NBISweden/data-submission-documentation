#!/bin/sh
java -jar ../webin-cli-6.5.0.jar -ascp -context reads -userName $1 -password $2 -manifest $3 -outputDir Webin_output/ -validate
