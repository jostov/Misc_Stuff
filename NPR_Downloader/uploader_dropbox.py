#!/usr/bin/python
# -*- coding: utf8 -*-
__author__ = 'fucckz'
__version__ = '1.0'

# import module not on current path
import sys

sys.path.append('../myDropbox')
import myDropbox

# import imp
# myDropbox = imp.load_source('util', '../myDropbox/myDropbox.py')

class DBuploader():
    def __init__(self):
        self.instance = myDropbox.DropboxTerm()

    def upload_by_chunk(self, from_file, file_path=None, overwrite=False):
        print "chunk uploading: ", from_file
        if (file_path == None):
            file_path = from_file.split('/')[-1]
        self.instance.do_put_by_chunks(from_file, file_path, 500 * 1024, overwrite) # 500kb per chunk

    def upload(self, from_file, file_path=None, overwrite=False):
        print "uploading: ", from_file
        if (file_path == None):
            file_path = from_file.split('/')[-1]
        self.instance.do_put(from_file, file_path, overwrite)


if __name__ == '__main__':
    print 'Nothing to see, go away..'