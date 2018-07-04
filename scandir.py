#!/usr/bin/python
#####################################################################################
#
# scandir.py
#
# Description: Scan directory privileges
#
# Author      : Fernando Diaz Sanchez <sirfids@gmail.com>
# Date        : 18 Jul 2014 
#
# How to use  : scandir.py <directorio>
#
#####################################################################################
import os
import sys
import stat
import pwd
import grp
from datetime import datetime

def processFile(currentDir):
    ''' Process files within this directory. '''
    # Get the absolute path of the currentDir
    currentDir = os.path.abspath(currentDir)

    # Get a list of files in currentDir
    try:
        filesInCurDir = os.listdir(currentDir)
    except OSError:
         return

    # Check all files
    for file in filesInCurDir:
        curFile = os.path.join(currentDir, file)
	# Check if it's a normal file or directory
        if os.path.isfile(curFile):
            # Get the file extension
            curFileExtension = curFile[-3:]
	else:
	    get_attr(curFile)
	    processFile(curFile)

def get_attr(curFile):
	# Check if it's a normal file or directory
        if os.path.isfile(curFile):
            # Get the file extension
            curFileExtension = curFile[-3:]
        else:
            try:
                statinfo = os.stat(curFile)
            except OSError:
                return
	    tam = get_size(curFile)
            tamc = get_human_size(tam)
            uid = get_uid_name(statinfo.st_uid)
            gid = get_group_name(statinfo.st_gid)
	    operm = get_other_perm(curFile,statinfo)
            gperm = get_group_perm(curFile,statinfo)
            uperm = get_owner_perm(curFile,statinfo)

	    text = "%s:%s:%s:%s:%s:%s:%s:%s:%s" % (curFile,
                    tam,statinfo.st_uid,uid,statinfo.st_gid,
                    gid,uperm,gperm,operm)
	    
	    print text

def get_uid_name(uid):
	try:
	   uidn = pwd.getpwuid(uid)[0]
	except KeyError:
	   uidn = "Unknown Owner"

	return uidn

def get_group_name(gid):
	try:
	   gidn = grp.getgrgid(gid)[0]
	except KeyError:
           gidn = "Unknown Group"

	return gidn

def get_other_perm(curFile,statinfo):
	is_read  = "-"
	is_write = "-"
	is_exec  = "-"

	if bool(statinfo.st_mode & stat.S_IROTH):
		is_read = "r"
	if bool(statinfo.st_mode & stat.S_IWOTH):
		is_write = "w"
	if bool(statinfo.st_mode & stat.S_IXOTH):
		is_exec = "x"

	result = is_read + is_write + is_exec
	
	return result

def get_group_perm(curFile,statinfo):	
        is_read  = "-"
        is_write = "-"
        is_exec  = "-"

        if bool(statinfo.st_mode & stat.S_IRGRP):
                is_read = "r"
        if bool(statinfo.st_mode & stat.S_IWGRP):
                is_write = "w"
        if bool(statinfo.st_mode & stat.S_IXGRP):
                is_exec = "x"

	result = is_read + is_write + is_exec
	
	return result

def get_owner_perm(curFile,statinfo):
        is_read  = "-"
        is_write = "-"
        is_exec  = "-"

        if bool(statinfo.st_mode & stat.S_IRUSR):
                is_read = "r"
        if bool(statinfo.st_mode & stat.S_IWUSR):
                is_write = "w"
        if bool(statinfo.st_mode & stat.S_IXUSR):
                is_exec = "x"

	result = is_read + is_write + is_exec
	
	return result

def get_name_size(tam):
	name_size = ""
	if (tam > 1024):
		if(tam > (1024 * 1024)):
			return "MB"
		else:
			return "KB"
	else:
		return "bytes"

def get_human_size(tam):
        name_size = ""
        if (tam > 1024):
                if(tam > (1024 * 1024)):
                        return (tam / 1024) / 1024
                else:
                        return tam / 1024
        else:
                return tam

def get_size(start_path='.'):
    total_size = 0
    seen = {}
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            try:
                stat = os.stat(fp)
            except OSError:
                continue

            try:
                seen[stat.st_ino]
            except KeyError:
                seen[stat.st_ino] = True
            else:
                continue

            total_size += stat.st_size

    return total_size
 
if __name__ == '__main__':
    
    # Get the current working directory
    currentDir = sys.argv[1]
    
    print "Path:Size:UID:Owner:GID:Group:PermOwner:PermGroup:PermOthers"

    # Start Processing
    get_attr(os.path.abspath(currentDir))
    processFile(currentDir)
 
