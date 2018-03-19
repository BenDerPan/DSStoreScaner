import json
import sys
import urllib
import io
from urllib.request import urlparse,urlopen
import os
import queue
import threading
from DSLib import DSStore
from urllib.request import quote,unquote

class DSScanner(object):
    '''
    基于.DS_Store文件的web物理路径结构扫描实现
    '''
    def __init__(self, start_url):
        self.queue = queue.Queue()
        self.queue.put(start_url)
        self.processed_url = set()
        self.lock = threading.Lock()
        self.working_thread = 0
        self.web_structure=None

    @property
    def Structures(self):
        return self.web_structure

    def process(self):
        while True:
            try:
                url = self.queue.get(timeout=2.0)
                self.lock.acquire()
                self.working_thread += 1
                self.lock.release()
            except Exception as e:
                if self.working_thread == 0:
                    break
                else:
                    continue
            try:
                if url in self.processed_url:
                    pass
                else:
                    self.processed_url.add(url)
                base_url = url.rstrip('.DS_Store')
                if not url.lower().startswith('http'):
                    url = 'http://%s' % url
                schema, netloc, path, _, _, _ = urlparse(url, 'http')
                try:
                    response = urlopen(url,timeout=5)

                except Exception as e:
                    if str(e) == 'HTTP Error 403: Forbidden':
                        folder_name = schema + "://" + netloc + '/'.join(path.split('/')[:-1])
                        self.lock.acquire()
                        if folder_name not in self.web_structure:
                            self.web_structure.append(unquote(folder_name))
                            print("[*]Found Folder:" + folder_name)
                        self.lock.release()
                    else:
                        # print (e)
                        pass
                data = response.read()

                if response.code == 200:
                    folder_name =schema+"://"+ netloc + '/'.join(path.split('/')[:-1])
                    self.lock.acquire()
                    if folder_name not in self.web_structure:
                        self.web_structure.append(unquote(folder_name))
                    self.lock.release()

                    if url.endswith('.DS_Store'):
                        ds_store_file = io.BytesIO()
                        ds_store_file.write(data)
                        d = DSStore.open(ds_store_file)

                        dirs_files = set()
                        for x in d.traverse():
                            dirs_files.add(x.filename)
                            fullName=folder_name+"/"+unquote(x.filename)
                            self.lock.acquire()
                            if fullName not in self.web_structure:
                                self.web_structure.append(fullName)
                                print("[*]Found File:" + folder_name + "/" + x.filename)
                            self.lock.release()


                        for name in dirs_files:
                            if name != '.':
                                self.queue.put(base_url + quote(name) + '/.DS_Store')
                        d.close()
            except Exception as e:
                # print(e)
                pass
            finally:
                self.working_thread -= 1

    def scan(self,thread_count=10):
        all_threads = []
        self.web_structure = []
        for i in range(thread_count):
            t = threading.Thread(target=self.process)
            all_threads.append(t)
            t.start()
        for task in all_threads:
            task.join()

def help_msg():
    print('''
=============================WelCome to use DSScaner==============================
DSScaner is used to check .DS_Store file exists, and it will try to walk through the web structure.

Useage: python DSScaner.py [target_url]

Examples:
\tpython python DSScaner.py http://localhost:8000/.DS_Store 
''')


if __name__ == '__main__':
    if len(sys.argv) != 2:
        help_msg()
        exit(-1)
    s = DSScanner(sys.argv[1])
    s.scan(thread_count=10)
    result=json.dumps(s.Structures, indent=4, ensure_ascii=False)
    print("=========================Web Physical File Structure==========================")
    print(result)
