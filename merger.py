#!/usr/local/bin/python

import getopt, sys
import os.path
import subprocess

from_dir = ""
to_dir = ""

def check_parameters():
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
		from_dir = os.path.abspath(from_dir)
		to_dir = os.path.abspath(to_dir)

	except getopt.error as err:
		print(str(err))
		sys.exit(2)

def get_relative_path(base_dir, target_dir):
	# print '[get_relative_path]base_dir:', base_dir
	# print '[get_relative_path]target_dir: ', target_dir
	common_prefix = os.path.commonprefix([base_dir, target_dir])
	rel_path = os.path.relpath(target_dir, common_prefix)
	return rel_path

def copy_file(src, target):
	try:
		subprocess.check_call(["lk", "-l"])
	except subprocess.CalledProcessError as e:
		print 'ERRRRRR', e.returncode, e.cmd, e.output

def iterate_files():
	for dirName, subdirList, fileList in os.walk(from_dir):
		if len(fileList) == 0:  
			continue
		print('Found directory: %s' % dirName)
		# TODO create target directory if needed
		
		for fname in fileList:
			print('\t%s' % get_relative_path(from_dir, dirName + os.path.sep + fname))



########################################
########################################
########################################

check_parameters()
#iterate_files()
copy_file('a', 'b')

print 'from_dir: ', from_dir
print 'to_dir: ', to_dir
print "DONE!"