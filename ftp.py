#!/usr/bin/env python
#coding=utf-8
# modifyDate: 20120808 ~ 20120810
# 鍘熶綔鑰呬负锛歜ones7456, http://li2z.cn/
# 淇敼鑰呬负锛歞ecli@qq.com
# v1.2锛宑hangeLog锛�
# +: 鏂囦欢鏃ユ湡/鏃堕棿/棰滆壊鏄剧ず銆佸绾跨▼鏀寔銆佷富椤佃烦杞�
# -: 瑙ｅ喅涓嶅悓娴忚鍣ㄤ笅涓婁紶鏂囦欢鍚嶄贡鐮侀棶棰橈細浠匢E锛屽叾瀹冩祻瑙堝櫒鏆傛椂娌″鐞嗐€�
# -: 涓€浜涜矾寰勬樉绀虹殑bug锛屼富瑕佹槸 cgi.escape() 杞箟闂
# ?: notepad++ 涓嬬洿鎺ョ紪璇戠殑server璺緞闂
 
"""
    绠€浠嬶細杩欐槸涓€涓� python 鍐欑殑杞婚噺绾х殑鏂囦欢鍏变韩鏈嶅姟鍣紙鍩轰簬鍐呯疆鐨凷impleHTTPServer妯″潡锛夛紝
    鏀寔鏂囦欢涓婁紶涓嬭浇锛屽彧瑕佷綘瀹夎浜唒ython锛堝缓璁増鏈�2.6~2.7锛屼笉鏀寔3.x锛夛紝
    鐒跺悗鍘诲埌鎯宠鍏变韩鐨勭洰褰曚笅锛屾墽琛岋細
        python SimpleHTTPServerWithUpload.py 1234       
    鍏朵腑1234涓轰綘鎸囧畾鐨勭鍙ｅ彿锛屽涓嶅啓锛岄粯璁や负 8000
    鐒跺悗璁块棶 http://localhost:1234 鍗冲彲锛宭ocalhost 鎴栬€� 1234 璇烽厡鎯呮浛鎹€�
"""
 
"""Simple HTTP Server With Upload.
 
This module builds on BaseHTTPServer by implementing the standard GET
and HEAD requests in a fairly straightforward manner.
 
"""
 
 
__version__ = "0.1"
__all__ = ["SimpleHTTPRequestHandler"]
__author__ = "bones7456"
__home_page__ = ""
 
import os, sys, platform
import posixpath
import BaseHTTPServer
from SocketServer import ThreadingMixIn
import threading
import urllib
import cgi
import shutil
import mimetypes
import re
import time
 
 
try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO
     
 
print ""
print '----------------------------------------------------------------------->> '
try:
   port = int(sys.argv[1])
except Exception, e:
   print '-------->> Warning: Port is not given, will use deafult port: 8000 '
   print '-------->> if you want to use other port, please execute: '
   print '-------->> python SimpleHTTPServerWithUpload.py port '
   print "-------->> port is a integer and it's range: 1024 < port < 65535 "
   port = 8912
    
if not 1024 < port < 65535:  port = 8090
serveraddr = ('', port)
print '-------->> Now, listening at port ' + str(port) + ' ...'
print '-------->> You can visit the URL:   http://localhost:' + str(port)
print '----------------------------------------------------------------------->> '
print ""
     
 
def sizeof_fmt(num):
    for x in ['bytes','KB','MB','GB']:
        if num < 1024.0:
            return "%3.1f%s" % (num, x)
        num /= 1024.0
    return "%3.1f%s" % (num, 'TB')
 
def modification_date(filename):
    # t = os.path.getmtime(filename)
    # return datetime.datetime.fromtimestamp(t)
    return time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(os.path.getmtime(filename)))
 
class SimpleHTTPRequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
 
    """Simple HTTP request handler with GET/HEAD/POST commands.
 
    This serves files from the current directory and any of its
    subdirectories.  The MIME type for files is determined by
    calling the .guess_type() method. And can reveive file uploaded
    by client.
 
    The GET/HEAD/POST requests are identical except that the HEAD
    request omits the actual contents of the file.
 
    """
 
    server_version = "SimpleHTTPWithUpload/" + __version__
 
    def do_GET(self):
        """Serve a GET request."""
        # print "....................", threading.currentThread().getName()
        f = self.send_head()
        if f:
            self.copyfile(f, self.wfile)
            f.close()
 
    def do_HEAD(self):
        """Serve a HEAD request."""
        f = self.send_head()
        if f:
            f.close()

    def do_PUT(self):
        """Serve a POST request."""
        r, info = self.deal_put_data()
        f = StringIO()
        f.write('success.')
        length = f.tell()
        f.seek(0)
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.send_header("Content-Length", str(length))
        self.end_headers()
        if f:
            self.copyfile(f, self.wfile)
            f.close()
 
    def do_POST(self):
        """Serve a POST request."""
        r, info = self.deal_post_data()
        print r, info, "by: ", self.client_address
        f = StringIO()
        f.write('<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">')
        f.write("<html>\n<title>Upload Result Page</title>\n")
        f.write("<body>\n<h2>Upload Result Page</h2>\n")
        f.write("<hr>\n")
        if r:
            f.write("<strong>Success:</strong>")
        else:
            f.write("<strong>Failed:</strong>")
        f.write(info)
        f.write("<br><a href=\"%s\">back</a>" % self.headers['referer'])
        f.write("<hr><small>Powered By: bones7456, check new version at ")
        f.write("<a href=\"http://li2z.cn/?s=SimpleHTTPServerWithUpload\">")
        f.write("here</a>.</small></body>\n</html>\n")
        length = f.tell()
        f.seek(0)
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.send_header("Content-Length", str(length))
        self.end_headers()
        if f:
            self.copyfile(f, self.wfile)
            f.close()
         
    def deal_put_data(self):
        remainbytes = int(self.headers['content-length'])
        path = self.translate_path(self.path)
        osType = platform.system()
        try:
            fn = os.path.join(path)
        except Exception, e:
            return (False, "鏂囦欢鍚嶈涓嶈鐢ㄤ腑鏂囷紝鎴栬€呬娇鐢↖E涓婁紶涓枃鍚嶇殑鏂囦欢銆�")
        if os.path.exists(fn):
            os.system("rm -rf fn")
        try:
            out = open(fn, 'wb')
        except IOError:
            return (False, "Can't create file to write, do you have permission to write?")

        while remainbytes > 0:
            line = self.rfile.readline()
            remainbytes -= len(line)
            out.write(line)
        out.close()
        return (True, "success.")

    def deal_post_data(self):
        print ("PlistText: ", self.headers)
        boundary = self.headers.plisttext.split("=")[1]
        remainbytes = int(self.headers['content-length'])
        line = self.rfile.readline()
        remainbytes -= len(line)
        if not boundary in line:
            return (False, "Content NOT begin with boundary")
        line = self.rfile.readline()
        remainbytes -= len(line)
        fn = re.findall(r'Content-Disposition.*name="file"; filename="(.*)"', line)
        if not fn:
            return (False, "Can't find out file name...")
        path = self.translate_path(self.path)
        osType = platform.system()
        try:
            fn = os.path.join(path, fn[0])
        except Exception, e:
            return (False, "鏂囦欢鍚嶈涓嶈鐢ㄤ腑鏂囷紝鎴栬€呬娇鐢↖E涓婁紶涓枃鍚嶇殑鏂囦欢銆�")
        if os.path.exists(fn):
            os.system("rm -rf fn")
        line = self.rfile.readline()
        remainbytes -= len(line)
        line = self.rfile.readline()
        remainbytes -= len(line)
        try:
            out = open(fn, 'wb')
        except IOError:
            return (False, "Can't create file to write, do you have permission to write?")
                 
        preline = self.rfile.readline()
        remainbytes -= len(preline)
        while remainbytes > 0:
            line = self.rfile.readline()
            remainbytes -= len(line)
            if boundary in line:
                preline = preline[0:-1]
                if preline.endswith('\r'):
                    preline = preline[0:-1]
                out.write(preline)
                out.close()
                return (True, "File '%s' upload success!" % fn)
            else:
                out.write(preline)
                preline = line
        return (False, "Unexpect Ends of data.")
 
    def send_head(self):
        """Common code for GET and HEAD commands.
 
        This sends the response code and MIME headers.
 
        Return value is either a file object (which has to be copied
        to the outputfile by the caller unless the command was HEAD,
        and must be closed by the caller under all circumstances), or
        None, in which case the caller has nothing further to do.
 
        """
        path = self.translate_path(self.path)
        f = None
        if os.path.isdir(path):
            if not self.path.endswith('/'):
                # redirect browser - doing basically what apache does
                self.send_response(301)
                self.send_header("Location", self.path + "/")
                self.end_headers()
                return None
            for index in "index.html", "index.htm":
                index = os.path.join(path, index)
                if os.path.exists(index):
                    path = index
                    break
            else:
                return self.list_directory(path)
        ctype = self.guess_type(path)
        try:
            # Always read in binary mode. Opening files in text mode may cause
            # newline translations, making the actual size of the content
            # transmitted *less* than the content-length!
            f = open(path, 'rb')
        except IOError:
            self.send_error(404, "File not found")
            return None
        self.send_response(200)
        self.send_header("Content-type", ctype)
        fs = os.fstat(f.fileno())
        self.send_header("Content-Length", str(fs[6]))
        self.send_header("Last-Modified", self.date_time_string(fs.st_mtime))
        self.end_headers()
        return f
 
    def list_directory(self, path):
        """Helper to produce a directory listing (absent index.html).
 
        Return value is either a file object, or None (indicating an
        error).  In either case, the headers are sent, making the
        interface the same as for send_head().
 
        """
        try:
            list = os.listdir(path)
        except os.error:
            self.send_error(404, "No permission to list directory")
            return None
        list.sort(key=lambda a: a.lower())
        f = StringIO()
        displaypath = cgi.escape(urllib.unquote(self.path))
        f.write('<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">')
        f.write("<html>\n<title>Directory listing for %s</title>\n" % displaypath)
        f.write("<body>\n<h2>Directory listing for %s</h2>\n" % displaypath)
        f.write("<hr>\n")
        f.write("<form ENCTYPE=\"multipart/form-data\" method=\"post\">")
        f.write("<input name=\"file\" type=\"file\"/>")
        f.write("<input type=\"submit\" value=\"upload\"/>")
        f.write("&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp")
        f.write("<input type=\"button\" value=\"HomePage\" onClick=\"location='/'\">")
        f.write("</form>\n")
        f.write("<hr>\n<ul>\n")
        for name in list:
            fullname = os.path.join(path, name)
            colorName = displayname = linkname = name
            # Append / for directories or @ for symbolic links
            if os.path.isdir(fullname):
                colorName = '<span style="background-color: #CEFFCE;">' + name + '/</span>'
                displayname = name
                linkname = name + "/"
            if os.path.islink(fullname):
                colorName = '<span style="background-color: #FFBFFF;">' + name + '@</span>'
                displayname = name
                # Note: a link to a directory displays with @ and links with /
            filename = os.getcwd() + '/' + displaypath + displayname
            f.write('<table><tr><td width="60%%"><a href="%s">%s</a></td><td width="20%%">%s</td><td width="20%%">%s</td></tr>\n'
                    % (urllib.quote(linkname), colorName,
                        sizeof_fmt(os.path.getsize(filename)), modification_date(filename)))
        f.write("</table>\n<hr>\n</body>\n</html>\n")
        length = f.tell()
        f.seek(0)
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.send_header("Content-Length", str(length))
        self.end_headers()
        return f
 
    def translate_path(self, path):
        """Translate a /-separated PATH to the local filename syntax.
 
        Components that mean special things to the local file system
        (e.g. drive or directory names) are ignored.  (XXX They should
        probably be diagnosed.)
 
        """
        # abandon query parameters
        path = path.split('?',1)[0]
        path = path.split('#',1)[0]
        path = posixpath.normpath(urllib.unquote(path))
        words = path.split('/')
        words = filter(None, words)
        path = os.getcwd()
        for word in words:
            drive, word = os.path.splitdrive(word)
            head, word = os.path.split(word)
            if word in (os.curdir, os.pardir): continue
            path = os.path.join(path, word)
        return path
 
    def copyfile(self, source, outputfile):
        """Copy all data between two file objects.
 
        The SOURCE argument is a file object open for reading
        (or anything with a read() method) and the DESTINATION
        argument is a file object open for writing (or
        anything with a write() method).
 
        The only reason for overriding this would be to change
        the block size or perhaps to replace newlines by CRLF
        -- note however that this the default server uses this
        to copy binary data as well.
 
        """
        shutil.copyfileobj(source, outputfile)
 
    def guess_type(self, path):
        """Guess the type of a file.
 
        Argument is a PATH (a filename).
 
        Return value is a string of the form type/subtype,
        usable for a MIME Content-type header.
 
        The default implementation looks the file's extension
        up in the table self.extensions_map, using application/octet-stream
        as a default; however it would be permissible (if
        slow) to look inside the data to make a better guess.
 
        """
 
        base, ext = posixpath.splitext(path)
        if ext in self.extensions_map:
            return self.extensions_map[ext]
        ext = ext.lower()
        if ext in self.extensions_map:
            return self.extensions_map[ext]
        else:
            return self.extensions_map['']
 
    if not mimetypes.inited:
        mimetypes.init() # try to read system mime.types
        extensions_map = mimetypes.types_map.copy()
        extensions_map.update({
        '': 'application/octet-stream', # Default
        '.py': 'text/plain;charset=UTF-8',
        '.c': 'text/plain;charset=UTF-8',
        '.h': 'text/plain;charset=UTF-8',
        '.txt': 'text/plain;charset=UTF-8',
        })
 
class ThreadingServer(ThreadingMixIn, BaseHTTPServer.HTTPServer):
    pass
     
def test(HandlerClass = SimpleHTTPRequestHandler,
       ServerClass = BaseHTTPServer.HTTPServer):
    BaseHTTPServer.test(HandlerClass, ServerClass)
 
if __name__ == '__main__':
    # test()
     
    #鍗曠嚎绋�
    # srvr = BaseHTTPServer.HTTPServer(serveraddr, SimpleHTTPRequestHandler)
     
    #澶氱嚎绋�
    srvr = ThreadingServer(serveraddr, SimpleHTTPRequestHandler)
    srvr.serve_forever() 

