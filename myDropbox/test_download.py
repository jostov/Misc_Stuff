#!/usr/bin/env python

import myDropbox

if __name__ == '__main__':
    term = myDropbox.DropboxTerm()
    term.do_get("newscast.mp3", "test.mp3") # use for testing
    print "[Download Finish]"
    print "Press any key to continue..."
    a=raw_input()
