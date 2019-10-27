#!/usr/local/bin/python

import getopt, sys
import os.path
import subprocess
import time

from_dir = ""
to_dir = ""
has_failure = False
total_file_size = 0
total_num_of_files = 0
total_num_of_failure = 0

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
	global total_num_of_files
	global total_file_size
	try:
		if file_is_exist(src, target):
			return
		subprocess.check_call(["cp", src, target])
		total_num_of_files += 1
		total_file_size += os.path.getsize(src)
		sys.stdout.write("Copying [files: {} ] [size: {}]\r".format(total_num_of_files, sizeof_fmt(total_file_size)))
		sys.stdout.flush()
	except Exception as e:
		print 'Copy Failure!', src, '->', target
		has_failure = True
		total_num_of_failure += 1

def create_folder_is_not_exist(path):
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
start_time = time.time()
check_parameters()
iterate_files()
if has_failure:
	print "DONE! Failure exists!"
else:
	print "\nDONE! Succes! ==> {} files copied! [{}]".format(total_num_of_files, sizeof_fmt(total_file_size))
print time.strftime("Time elapsed: %H:%M:%S", time.gmtime(time.time() - start_time))


