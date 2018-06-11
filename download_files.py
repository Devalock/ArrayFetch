import requests
from lxml import etree
from PyQt5 import QtCore
import re
import os
import time
html_base = "http://ftp.ebi.ac.uk/pub/databases/arrayexpress/data/experiment/"
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0"}
re_catagory = re.compile(r"-(.*)-")


def set_download(set, str1, str2):
    global download_set
    global file_position
    global input_keyword
    download_set = set
    file_position = str1
    input_keyword = str2

def download(acc):
    catagory = re.search(re_catagory, acc).group(1)
    url = html_base + catagory + "/" + acc + "/"
    html = etree.HTML(
        requests.get(url, headers=headers).text)
    files = html.xpath("//td/a/@href")
    files = files[1::]
    print(files)
    if os.path.exists(file_position + "\\" + input_keyword + "\\" + "download"):
        pass
    else:
        os.mkdir(file_position + "\\" + input_keyword + "\\" + "download")
    for i in files:
        if re.search(".*txt", i):
            print(url + i)
            r = requests.get(url + i, stream=True, headers=headers)
            with open(file_position + "\\" + input_keyword + "\\" + "download" + "\\" + i, "wb") as f:
                for line in r.iter_lines():
                    if line:
                        f.write(line)
                        f.write("\r\n".encode(encoding="utf-8"))
        else:
            print(url + i)
            r = requests.get(url + i, stream=True, headers=headers)
            with open(file_position + "\\" + input_keyword + "\\" + "download" + "\\" + i, "wb") as f:
                for chunk in r.iter_content(1024):
                    f.write(chunk)


class Job(QtCore.QThread):
    signal = QtCore.pyqtSignal(str, int)

    def __init__(self, rest):
        super(Job, self).__init__()
        self.rest = rest

    def __del__(self):
        self.wait()

    def run(self):
        start_time = time.time()
        progress = "start! downloading..."
        self.signal.emit(progress, 0)
        experiment_count = len(download_set)
        count = 0
        for i in download_set:
            count += 1
            download(i)
            time.sleep(self.rest)
            time_left = int(
                (time.time() - start_time) / count * (experiment_count - count + 1))
            progress = str(count) + " of " + str(experiment_count) + " time left: " + str(
                time_left) + "seconds"
            rate = int((count / experiment_count) * 100)
            self.signal.emit(progress, rate)
        end_time = time.time()
        last_time = int(end_time - start_time)
        progress = ("end. time used: %s seconds" % last_time)
        self.signal.emit(progress, 100)




