#!/usr/local/bin/python

import getopt, sys
import os.path
import subprocess

from_dir = ""
to_dir = ""
has_failure = False

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
		arguments, values = getopt.getopt(argumentList, unixOptions, gnuOptions)
		
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
	global has_failure
	try:
		subprocess.check_call(["cp", src, target])
		# print 'cp', src , '->', target
	except:
		print 'Copy Failure!', src, '->', target
		has_failure = True


def create_folder_is_not_exist(path):
	if not os.path.exists(path):
		os.makedirs(path)

def iterate_files():
	for dirName, subdirList, fileList in os.walk(from_dir):
		if len(fileList) == 0:  
			continue
		
		relative_target_folder = get_relative_path(from_dir, dirName)
		# print('Found relative_target_folder: %s' % relative_target_folder)
		# print('Found absolute directory: %s' % dirName)
		# TODO create target directory if needed
		create_folder_is_not_exist(os.path.join(to_dir, relative_target_folder))

		for fname in fileList:
			# print('\t%s' % get_relative_path(from_dir, os.path.join(dirName, fname)))
			absolute_src_file = os.path.join(dirName, fname)
			relative_src_file = get_relative_path(from_dir, absolute_src_file)

			# print('\t%s' % relative_src_file)
			absolute_target_file = os.path.join(to_dir, relative_src_file)
			copy_file(absolute_src_file, absolute_target_file)

########################################
########################################
########################################

check_parameters()
iterate_files()
if has_failure:
	print "DONE! Failure exists!"
else:
	print "DONE! No Failure"