# -*- coding: utf-8 -*-
__author__ = 'fucckz'

import os
import uploader_filemanager

if __name__ == '__main__':
    rootDir="download/"
    list_dirs = os.walk(rootDir)
    uploader=uploader_filemanager.FMuploader()
    uploader.search_lan_for_devices()
    for root, dirs, files in list_dirs:
        for f in files:
            file_path=os.path.join(root, f)
            try:
                status=uploader.upload(file_path, 'NPR/')
                if status==302: # HTTP 302 - Found
                    print " - success"
                else:
                    print " - fail"
            except:
                print " - error"
                pass
    print 'done!'
