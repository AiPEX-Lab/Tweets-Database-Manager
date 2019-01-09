#!/bin/bash
echo ""
for file in ../data/*.geojson
do
	echo "$file"
	head -c 30 "$file"
	echo "" # new line
	tail -c 30 "$file"
	echo "" # new line
	echo "------------"
	echo ""
done
