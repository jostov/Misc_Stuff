#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'fucckz'
__version__ = 'sample'
import requests
import os
import sys

if __name__ == '__main__':
    if len(sys.argv)<2:
        print 'Please specify audio file'
        sys.exit(0)

    print('Uploading Audio File: ' + sys.argv[1])
    audio=open(sys.argv[1], "rb")
    headers = {
        "Content-Type": "audio/x-flac; rate=16000",
        # "User-Agent": "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.17 Safari/537.36", # UA: Chrome 30.0.1599.17
        "Accept-Encoding": "",  # removing useless headers that causing false response
        "Accept": "",   # removing useless headers that causing false response
    }
    url = "https://www.google.com/speech-api/v1/recognize?xjerr=1&client=chromium&lang=en-US"
    # url = "http://httpbin.org/post"   # testing post url

    r = requests.post(url, data=audio, headers=headers)
    # print r.headers
    print r.status_code
    print r.json()
    audio.close()

    if (os.name=='nt'):
        os.system('pause')