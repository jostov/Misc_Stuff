#!/usr/bin/env python

import locale
import os
import pprint
import shlex
import sys

from dropbox import client, rest


class DropboxTerm():
    ABS_PATH = os.path.dirname(os.path.abspath(__file__)) + "/"
    TOKEN_FILE = ABS_PATH + "auth_files/token_store.txt"
    APP_KEY_FILE = ABS_PATH + "auth_files/app_key_store.txt"
    APP_SECRET_FILE = ABS_PATH + "auth_files/app_secret_store.txt"

    def __init__(self, login=False):
        """

        :param login:
        """
        self.current_path = ''
        self.api_client = None
        self.app_key = None
        self.app_secret = None

        if (login == True):
            # read app key
            try:
                appkey = open(self.APP_KEY_FILE).read()
                self.app_key = appkey
                print "[loaded app key]"
            except IOError:
                exit("Error: app_key_store.txt missing!")
                # read app secret
            try:
                appsecret = open(self.APP_SECRET_FILE).read()
                self.app_secret = appsecret
                print "[loaded app secret]"
            except IOError:
                exit("Error: app_secret_store.txt missing!")

        try:
            token = open(self.TOKEN_FILE).read()
            self.api_client = client.DropboxClient(token)
            print "[loaded access token]"
        except IOError as err:
            print os.getcwd()
            print err
            exit("Error: token_store.txt missing!")

    def do_ls(self):
        """list files in current remote directory"""
        resp = self.api_client.metadata(self.current_path)

        if 'contents' in resp:
            for f in resp['contents']:
                name = os.path.basename(f['path'])
                encoding = locale.getdefaultlocale()[1]
                self.stdout.write(('%s\n' % name).encode(encoding))


    def do_cd(self, path):
        """change current working directory"""
        if path == "..":
            self.current_path = "/".join(self.current_path.split("/")[0:-1])
        else:
            self.current_path += "/" + path


    def do_login(self):
        """log in to a Dropbox account"""
        flow = client.DropboxOAuth2FlowNoRedirect(self.app_key, self.app_secret)
        authorize_url = flow.start()
        sys.stdout.write("1. Go to: " + authorize_url + "\n")
        sys.stdout.write("2. Click \"Allow\" (you might have to log in first).\n")
        sys.stdout.write("3. Copy the authorization code.\n")
        code = raw_input("Enter the authorization code here: ").strip()

        try:
            access_token, user_id = flow.finish(code)
        except rest.ErrorResponse, e:
            self.stdout.write('Error: %s\n' % str(e))
            return

        with open(self.TOKEN_FILE, 'w') as f:
            f.write(access_token)
        self.api_client = client.DropboxClient(access_token)


    def do_logout(self):
        """log out of the current Dropbox account"""
        self.api_client = None
        os.unlink(self.TOKEN_FILE)
        self.current_path = ''


    def do_cat(self, path):
        """display the contents of a file"""
        f, metadata = self.api_client.get_file_and_metadata(self.current_path + "/" + path)
        self.stdout.write(f.read())
        self.stdout.write("\n")


    def do_mkdir(self, path):
        """create a new directory"""
        self.api_client.file_create_folder(self.current_path + "/" + path)


    def do_rm(self, path):
        """delete a file or directory"""
        self.api_client.file_delete(self.current_path + "/" + path)


    def do_mv(self, from_path, to_path):
        """move/rename a file or directory"""
        self.api_client.file_move(self.current_path + "/" + from_path,
                                  self.current_path + "/" + to_path)


    def do_share(self, path):
        print self.api_client.share(path)['url']


    def do_account_info(self):
        """display account information"""
        f = self.api_client.account_info()
        pprint.PrettyPrinter(indent=2).pprint(f)


    def do_exit(self):
        """exit"""
        return True


    def do_get(self, from_path, to_path):
        """
        Copy file from Dropbox to local file and print out the metadata.

        """
        to_file = open(os.path.expanduser(to_path), "wb")

        f, metadata = self.api_client.get_file_and_metadata(self.current_path + "/" + from_path)
        print 'Metadata:', metadata
        to_file.write(f.read())

    def do_get_by_chunks(self, from_path, to_path, chuncksize):
        """
        Copy file from Dropbox to local file and print out the metadata by chunks.

        """
        to_file = open(os.path.expanduser(to_path), "wb")

        from_path = self.current_path + "/" + from_path
        f, metadata = self.api_client.get_file_and_metadata(from_path)
        # print 'Metadata:', metadata
        file_size = metadata['bytes']
        print "Downloading: %s Bytes: %s" % (from_path, file_size)

        file_size_dl = 0
        while True:
            buffer = f.read(chuncksize)
            if not buffer:
                break
            file_size_dl += len(buffer)
            to_file.write(buffer)
            status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
            # status = status + chr(8)*(len(status)+1)
            status += chr(13)
            print status,
        print ''
        to_file.close()

    def do_thumbnail(self, from_path, to_path, size='large', format='JPEG'):
        """
        Copy an image file's thumbnail to a local file and print out the
        file's metadata.

        Examples:
        Dropbox> thumbnail file.txt ~/dropbox-file.txt medium PNG
        """
        to_file = open(os.path.expanduser(to_path), "wb")

        f, metadata = self.api_client.thumbnail_and_metadata(
            self.current_path + "/" + from_path, size, format)
        print 'Metadata:', metadata
        to_file.write(f.read())


    def do_put(self, from_path, to_path, overwrite=False):
        """
        Copy local file to Dropbox

        """
        from_file = open(os.path.expanduser(from_path), "rb")

        self.api_client.put_file(self.current_path + "/" + to_path, from_file, overwrite)


    def do_put_by_chunks(self, from_path, to_path, chunk_size, overwrite=False):
        """
        Copy local file to Dropbox by chuncks

        """

        # get file size
        from_file = open(os.path.expanduser(from_path), "rb")
        from_file.seek(0, 2)
        size = from_file.tell()
        from_file.seek(0)

        uploader = self.api_client.get_chunked_uploader(from_file, size)
        while uploader.offset < size:
            try:
                upload = uploader.upload_chunked(chunk_size)
            except rest.ErrorResponse, e:
                # perform error handling and retry logic
                print e
        uploader.finish(self.current_path + "/" + to_path, overwrite)


    def do_search(self, string):
        """Search Dropbox for filenames containing the given string."""
        results = self.api_client.search(self.current_path, string)
        for r in results:
            self.stdout.write("%s\n" % r['path'])


    def do_help(self):
        # Find every "do_" attribute with a non-empty docstring and print
        # out the docstring.
        all_names = dir(self)
        cmd_names = []
        for name in all_names:
            if name[:3] == 'do_':
                cmd_names.append(name[3:])
        cmd_names.sort()
        for cmd_name in cmd_names:
            f = getattr(self, 'do_' + cmd_name)
            if f.__doc__:
                self.stdout.write('%s: %s\n' % (cmd_name, f.__doc__))


    # the following are for command line magic and aren't Dropbox-related
    def emptyline(self):
        pass

    def do_EOF(self, line):
        self.stdout.write('\n')
        return True

    def parseline(self, line):
        parts = shlex.split(line)
        if len(parts) == 0:
            return None, None, line
        else:
            return parts[0], parts[1:], line


if __name__ == '__main__':
    term = DropboxTerm(True)
    while True:
        try:
            term.do_login()
        except:
            print "Error, please retry..."
        else:
            break
    print "See 'auth_files/token_store.txt' for token detail, press any key to continue..."
    a = raw_input()