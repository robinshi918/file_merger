# file_merger
merge files from one folder to another.
- create the folder structure in target folder
- if target file already exists, do md5 to check the file integraty. If md5 is same, skip and continue. If md5 is not different, report an error and continue. 
- if target fiel does not exist, copy it.
- if there is error copying file, report an error and skip it.
