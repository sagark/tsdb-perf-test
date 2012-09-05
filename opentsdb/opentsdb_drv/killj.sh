#!/bin/sh

#DO NOT PUT java in the filename of this file
OJAVA=$(pgrep -o java)
NJAVA=$(pgrep -n -l java)
echo $OJAVA
echo $NJAVA
while [ "$OJAVA" != "$NJAVA" ]
do
	echo "LOL"
	pkill -o java
	OJAVA=$(pgrep -o java)
	NJAVA=$(pgrep -n java)
done
