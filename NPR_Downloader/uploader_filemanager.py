#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'fucckz'
__version__ = '1.0'

import poster

class FMuploader():
    def __init__(self):
        self.host=""
        # poster.do_patch_http_response_read()    # patch http.response.read() function
        print "[FMuploader Init]"

    def search_lan_for_devices(self):
        self.host = "192.168.1.8"
        # TODO: add this part
        print ""

    def post_multi_encoded_file(self, file_path, remote_path=None):
        """
        remote_path must contains directory only, and is case-sensitive

        example:
            remote_path="sample_folder/"

        directory of remote_path must exists in remote to avoid unexpected errors
        """
        file_name = file_path.split('/')[-1]
        data = open(file_path, "rb").read()
        if remote_path!=None and remote_path[-1]=='/':
            file_name=remote_path+file_name
        res=poster.post_multipart(self.host, 8080, '/files', [], [('newfile', file_name, data)])
        return res.status


    def upload(self, from_file, remote_path=None):
        print 'uploading: ', from_file,
        return self.post_multi_encoded_file(from_file, remote_path)


if __name__ == '__main__':
    print 'Nothing to see, go away..'