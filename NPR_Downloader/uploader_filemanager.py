#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'fucckz'
__version__ = '1.0'

import poster

class FMuploader():
    def __init__(self):
        poster.do_patch_http_response_read()
        print "[FMuploader Init]"

    def search_lan_for_devices(self):
        # TODO: add this part
        print ""

    def post_multi_encoded_file(self, file_path):\
        # TODO: remove hardcode variables
        host = "192.168.1.8"
        data = open(file_path, "rb").read()
        poster.do_patch_http_response_read()
        res=poster.post_multipart(host, 8080, '/files', [], [('newfile', 'news.mp3', data)])
        print res.read()
        print res.status


    def upload(self, from_file):
        print 'uploading: ', from_file
        self.post_multi_encoded_file(from_file)


if __name__ == '__main__':
    uploader = FMuploader()
    uploader.upload('download/aaa.mp3')
    print 'done!'