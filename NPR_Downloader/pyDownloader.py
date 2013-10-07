#!/usr/bin/python
# -*- coding: utf8 -*-
__author__ = 'fucckz'
__version__ = '1.0'

import urllib2


def download(url, file_path=None):
    # url = "http://pd.npr.org/anon.npr-mp3/npr/tmm/2013/10/20131007_tmm_05.mp3"
    if (file_path == None):
        file_path = url.split('/')[-1]
    u = urllib2.urlopen(url)
    f = open(file_path, 'wb')
    meta = u.info()
    file_size = int(meta.getheaders("Content-Length")[0])
    print "Downloading: %s Bytes: %s" % (file_path, file_size)

    file_size_dl = 0
    block_sz = 8192
    while True:
        buffer = u.read(block_sz)
        if not buffer:
            break
        file_size_dl += len(buffer)
        f.write(buffer)
        status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
        # status = status + chr(8)*(len(status)+1)
        status += chr(13)
        print status,
    print ''
    f.close()


if __name__ == '__main__':
    print 'Nothing to see, go away..'