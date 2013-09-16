#!/usr/bin/python
# -*- coding: utf8 -*-
__author__ = 'fucckz'
__version__ = '0.1'
__DEFAULT_DOWNLOAD_DIR__ = "./download"
import sys
import Queue
import threading
import os
import urlparse
import httplib
from datetime import date
from datetime import datetime
import getopt


class downloader(threading.Thread):
    def __init__(self, que):
        threading.Thread.__init__(self)
        self.que = que

    def run(self):
        while True:
            if not self.que.empty():
                print('-----%s------' % (self.name))
                file_url=self.que.get()
                os.system('curl -o ./download/' + urlparse.urlparse(file_url).path.split('/')[-1] + " " + file_url)
            else:
                break


def getHeader(ourl):
    url = urlparse.urlparse(ourl)
    conn = httplib.HTTPConnection(url.netloc)
    conn.request("HEAD", url.path)
    res = conn.getresponse()
    return res


def generateList_NPR(programs):
    global download_date
    # generate url
    dQueue = Queue.Queue()
    # puts Hourly News Summary into queue
    dQueue.put("http://public.npr.org/anon.npr-mp3/npr/news/newscast.mp3")
    if (download_date==None):
        download_date = date.today()
    programs=programs.split(',')
    for program in programs:
        program=program.strip()
        print "checking program: " + program
        url_left = "http://pd.npr.org/anon.npr-mp3/npr/" + program + download_date.strftime("/%Y/%m/%Y%m%d_") + program + "_"
        url_right = ".mp3"

        # check url availability
        i = 1
        while True:
            url_temp = url_left + str(i).rjust(2, '0') + url_right
            if (os.path.exists("./download/" + urlparse.urlparse(url_temp).path.split('/')[-1])):
                i += 1
                continue

            res = getHeader(url_temp)
            if (res.status == 200):
                # filter out empty file
                if (res.getheader("Content-Length") == "0" or res.getheader("Content-Length") == None):
                    i += 1
                    continue
                print(url_temp)
                dQueue.put(url_temp)
                i += 1
            else:
                break
    return dQueue


if __name__ == '__main__':
    print("Radio Downloader v" + __version__)
    # process parameters
    # TODO: add -k --keep_output_structure, -c --clear_download_folder
    try:
        opts, args = getopt.getopt(sys.argv[1:], "d:hvp:t:", ["date=", "help", "version", "program=", "task="])
    except getopt.GetoptError as err:
        # print help information and exit:
        print str(err) # will print something like "option -a not recognized"
        sys.exit(2)
    programs = None
    download_date = None
    task = 1
    for o, a in opts:
        if o in ("-v", "--version"):
            print __version__
            sys.exit()
        elif o in ("-h", "--help"):
            print("Currently under construction...")
            sys.exit()
        elif o in ("-p", "--program"):
            programs = a
        elif o in ("-d", "--date"):
            download_date = a
            download_date = datetime.strptime(download_date, "%d%m%y").date()
        elif o in ("-t", "--task"):
            task=int(a)
            print("multi-task downlod: " + a)
        else:
            assert False, "unhandled option"

    if programs == None:
        programs="me,atc,fa,tmm,ama,ted,waitwait"
    # ...

    # check directory exist
    if not os.path.isdir(__DEFAULT_DOWNLOAD_DIR__):
        print("download directory doesn't exist, create one at: " + __DEFAULT_DOWNLOAD_DIR__)
        os.makedirs(__DEFAULT_DOWNLOAD_DIR__)

    # download...
    dQueue = generateList_NPR(programs)
    for i in range(task):
        d=downloader(dQueue)
        d.start()
    print("FINISH")