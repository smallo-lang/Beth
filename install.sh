#!/usr/bin/bash

LOCATION="/usr/local/bin/"

pyinstaller main.py --onefile

if [ -d dist ]; then
	# install by adding to PATH
	sudo mv dist/main $LOCATION

	# cleanup
	rm -r dist build __pycache__
	rm *.spec
fi

