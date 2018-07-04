# [scandir](https://bluenix.pe/tools/scripts/scandir.html)
![version](https://img.shields.io/badge/version-1.0.0-blue.svg) ![license](https://img.shields.io/badge/license-MIT-green.svg)

scandir is a small and fast script to scan privileges on directories and dump this data as csv like text in order to manipulate it later.

## Requirements
* Python 2.4.3 o superior

## How to use scandir.py

	./scandir.py <dir>

	Examples: Show /home/fids folder info

	./scandir.py /home/fids


## Value returns

	Path: Directory path
	Size: Size in bytes
	UID: Directory UID
	Owner: Directory Owner
	GID: Directory GID
	Group: Directory Group	
    PermOwner: Owner privileges
	PermGroup: Group privileges
	PermOthers: Other privileges

	This values are separated by hypen (:) character
