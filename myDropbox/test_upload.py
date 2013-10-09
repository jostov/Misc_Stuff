#!/usr/bin/env python

import myDropbox

if __name__ == '__main__':
    term = myDropbox.DropboxTerm()
    term.do_put_by_chunks("test.mp3", "222.mp3", 500 * 1024) # use for testing
    print "[Upload Finish]"
    print "Press any key to continue..."
    a = raw_input()