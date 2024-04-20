#!/bin/sh

(test -d src) || {
	echo "*** ERROR: src directory not found! ***"
	exit 1
}

(test -e configure.ac) || {
	echo "*** ERROR: configure.ac file not found! ***"
	exit 1
}

./configure
