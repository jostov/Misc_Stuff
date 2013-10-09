#!/usr/bin/python
# -*- coding: utf8 -*-
__author__ = 'fucckz'
__version__ = '0.2'
import sys
import Queue
import threading
import os
import urlparse
import httplib
from datetime import date
from datetime import datetime
import getopt
import platform
import pyDownloader


class downloader(threading.Thread):
    global download_command

    def __init__(self, que):
        threading.Thread.__init__(self)
        self.que = que

    def run(self):
        while True:
            if not self.que.empty():
                print('-----%s------' % (self.name))
                file_url = self.que.get()
                if (download_command != None):
                    os.system(download_command + ' ' + download_output + urlparse.urlparse(file_url).path.split('/')[
                        -1] + " " + file_url)
                else:
                    pyDownloader.download(file_url)
            else:
                break


def getSystemInfo():
    return platform.system()


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
    if (download_date == None):
        download_date = date.today()
    programs = programs.split(',')
    for program in programs:
        program = program.strip()
        print "checking program: " + program
        url_left = "http://pd.npr.org/anon.npr-mp3/npr/" + program + download_date.strftime(
            "/%Y/%m/%Y%m%d_") + program + "_"
        url_right = ".mp3"

        # check url availability
        i = 1
        while True:
            url_temp = url_left + str(i).rjust(2, '0') + url_right
            if (os.path.exists(download_output + urlparse.urlparse(url_temp).path.split('/')[-1])):
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
        opts, args = getopt.getopt(sys.argv[1:], "d:hvp:t:o:n",
                                   ["date=", "help", "version", "program=", "task=", "-output-document=", "not-upload"])
    except getopt.GetoptError as err:
        # print help information and exit:
        print str(err) # will print something like "option -a not recognized"
        sys.exit(2)
    programs = None
    download_date = None
    download_command = None
    download_output = None
    needs_upload = True
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
            download_date = datetime.strptime(download_date, "%m%d%y").date()
        elif o in ("-t", "--task"):
            task = int(a)
            print("multi-task downlod: " + a)
        elif o in ("-o", "--output-document"):
            download_output = a
        elif o in ("-n", "--not-upload"):
            needs_upload = False
        else:
            assert False, "unhandled option"

    # default values
    if programs == None:
        programs = "me,atc,fa,tmm,ama,ted,waitwait"
    if download_output == None:
        download_output = './download/'
        # ...

    # check os info
    osStr = getSystemInfo()
    if (osStr == "Windows"):  #for windows
        download_command = 'wget -O'  #same as "--output-document=file"
    elif (osStr == "Darwin"): # for mac
        download_command = 'curl -o'
    elif (osStr == "Linux"):   # for linux distros
        try:
            import androidhelper
        except:
            download_command = 'wget -O'
        else:
            # on Android QPython
            osStr = 'Android'
            download_command = None
    else: # unknow system...
        osStr = 'Unknown'
        download_command = 'wget -O'
    print osStr

    # check directory exist
    if not os.path.isdir(download_output[:-1]):
        print("download directory doesn't exist, create one at: " + download_output[:-1])
        os.makedirs(download_output[:-1])

    # download...
    dQueue = generateList_NPR(programs)
    threads=[]
    for i in range(task):
        d = downloader(dQueue)
        threads.append(d)
        d.start()
    print("---download finish!---")

    # wait till all the threads will
    for thread in threads:
        thread.join()

    # upload...
    if (needs_upload==True):
        import subprocess
        subprocess.Popen("DBupload.py", shell=True)

    print("FINISH")