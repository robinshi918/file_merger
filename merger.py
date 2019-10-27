#!/usr/local/bin/python

import getopt, sys
import os.path
import subprocess
import time

# global variables
from_dir = ""
to_dir = ""
has_failure = False

# total
total_size_of_files = 0
total_num_of_files = 0
total_num_of_failure = 0

# copied
total_num_of_copied_files = 0
total_size_of_copied_files = 0

'''
Check if target file already exist.
Return True if target file already exist and has same content with src file.
Otherwise return False
'''
def file_is_exist(src, dst):
	if os.path.exists(dst):
		try:
			src_checksum = subprocess.check_output(["/sbin/md5", "-q", src])
			dst_checksum = subprocess.check_output(["/sbin/md5", "-q", dst])
			if src_checksum == dst_checksum:
				return True
		except Exception as e:
			return False
	return False

'''
check if command line parameters are valid
'''
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

string_on_screen = ""
def copy_file(src, target):
	global total_num_of_files
	global total_num_of_failure
	global total_size_of_files
	global total_num_of_copied_files
	global total_size_of_copied_files
	global string_on_screen
	
	try:
		# clear previous string from screen
		back_str = '\b'*len(string_on_screen)
		# print string_on_screen
		sys.stdout.write(back_str)
		

		total_num_of_files += 1
		file_size = os.path.getsize(src)
		total_size_of_files += file_size
		string_on_screen = "Verifying [files: {} ] [size: {}]\t{}\r".format(total_num_of_files, sizeof_fmt(total_size_of_files), src)
		sys.stdout.write(string_on_screen)
		sys.stdout.flush()
		
		if file_is_exist(src, target):
			return

		subprocess.check_call(["cp", src, target])
		total_num_of_copied_files += 1
		total_size_of_copied_files += file_size
		string_on_screen = "Copying [files: {} ] [size: {}]\t{}\r".format(total_num_of_copied_files, sizeof_fmt(total_size_of_copied_files), src)
		sys.stdout.write(string_on_screen)
		sys.stdout.flush()

	except Exception as e:
		print 'Error!', src, '->', target
		print e.message
		total_num_of_failure += 1
		

def create_folder_if_not_exist(path):
	if not os.path.exists(path):
		os.makedirs(path)

def sizeof_fmt(num, suffix='B'):
    for unit in ['','K','M','G','T','P','E','Z']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)

def iterate_files():
	print "Starting Copy!"
	for dirName, subdirList, fileList in os.walk(from_dir):
		if len(fileList) == 0:  
			continue
		
		relative_target_folder = get_relative_path(from_dir, dirName)
		create_folder_if_not_exist(os.path.join(to_dir, relative_target_folder))

		for fname in fileList:
			absolute_src_file = os.path.join(dirName, fname)
			relative_src_file = get_relative_path(from_dir, absolute_src_file)

			absolute_target_file = os.path.join(to_dir, relative_src_file)
			copy_file(absolute_src_file, absolute_target_file)

start_time = time.time()
check_parameters()
iterate_files()

print "\n\n=========== MISSION COMPLETE ==========="
print "Total Files: \t\t{}\t[{}]".format(total_num_of_files,sizeof_fmt(total_size_of_files))
print "Files Copied: \t\t{}\t[{}]".format(total_num_of_copied_files, sizeof_fmt(total_size_of_copied_files))
print "Num of Failures:\t{}".format(total_num_of_failure)
print time.strftime("Time elapsed: \t\t%H:%M:%S", time.gmtime(time.time() - start_time))
print
