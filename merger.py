#!/usr/local/bin/python

import getopt, sys
import os.path

from_dir = ""
to_dir = ""

def checkParameters():
	global from_dir
	global to_dir
	fullCmdArguments = sys.argv

	argumentList = fullCmdArguments[1:]
	if len(argumentList) != 4:
		print "IllegalArgument"
		sys.exit(2)

	unixOptions = "f:t:"
	gnuOptions = ["from=", "to="]

	try:
		arguments, values = getopt.getopt(argumentList, unixOptions, gnuOptions)\
		
		# get values from command parameter	
		for currentArgument, currentValue in arguments:
			if currentArgument in ("-f", "--from"):
				from_dir = currentValue
			elif currentArgument in ("-t", "--to"):
				to_dir = currentValue
		
		# check folder existence
		if not os.path.exists(from_dir):
			print (("source folder does not exist! (%s)")%(from_dir))
			sys.exit(2)
		if not os.path.exists(to_dir):
			print (("target folder does not exist! (%s)")%(to_dir))
			sys.exit(2)

	except getopt.error as err:
		print(str(err))
		sys.exit(2)

def iterate_files():
	for dirName, subdirList, fileList in os.walk(from_dir):
		print('Found directory: %s' % dirName)
    	for fname in fileList:
        	print('\t%s' % fname)

########################################
########################################
########################################

checkParameters()
iterate_files()

print from_dir
print to_dir
print "DONE!"