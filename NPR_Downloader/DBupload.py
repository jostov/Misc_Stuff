# -*- coding: utf-8 -*-
__author__ = 'fucckz'

import os
import uploader_dropbox

if __name__ == '__main__':
    rootDir="download/"
    list_dirs = os.walk(rootDir)
    uploader=uploader_dropbox.DBuploader()
    for root, dirs, files in list_dirs:
        for f in files:
            file_path=os.path.join(root, f)
            uploader.upload(file_path, None, True)
    print 'done!'
