import Main_spider
import re
import requests
import time
import os
from lxml import etree
from PyQt5 import QtCore


def set_requires(str1, str2):
    global input_keyword
    global file_position
    input_keyword = str1
    file_position = str2


class Job(QtCore.QThread):
    signal = QtCore.pyqtSignal(str, int)

    def __init__(self, rest, mode):
        super(Job, self).__init__()
        self.rest = rest
        self.mode = mode

    def __del__(self):
        self.wait()

    def run(self):
        progress = "start! connecting to ArrayExpress..."
        self.signal.emit(progress, 0)
        url = "https://www.ebi.ac.uk/arrayexpress/xml/v3/experiments"
        keywords = {"keywords": input_keyword}
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0"}
        r = requests.get(url, params=keywords, headers=headers)

        page = etree.fromstring(r.content)
        accs = page.xpath("experiment/accession/text()")
        print(accs)
        accession_numbers = len(accs)
        extract_pattern = re.compile(r"\s*(cancer|carcinoma|or|and)\s*", re.I)
        extract = re.sub(extract_pattern, " ", input_keyword).split(" ")
        extract_set = set()
        for i in extract:
            if re.match(r"\S+", i):
                extract_set.add(i)

        start_time = time.time()
        experiment_count = 0
        file_existence = [1, 2, 3, 4]
        if os.path.exists(file_position + "\\" + input_keyword + "\\accs\\"):
            pass
        else:
            os.mkdir(file_position + "\\" + input_keyword + "\\accs\\")
        try:
            f = open(file_position + "\\" + input_keyword + "\\accs\\" + input_keyword + "_accs_nml.txt")
            f.close()
        except IOError:
            file_existence.remove(1)
        try:
            f = open(file_position + "\\" + input_keyword + "\\accs\\" + input_keyword + "_accs_clf.txt")
            f.close()
        except IOError:
            file_existence.remove(2)
        try:
            f = open(file_position + "\\" + input_keyword + "\\accs\\" + input_keyword + "_accs_nst.txt")
            f.close()
        except IOError:
            file_existence.remove(3)
        try:
            f = open(file_position + "\\" + input_keyword + "\\accs\\" + input_keyword + "_accs_raw.txt")
            f.close()
        except IOError:
            file_existence.remove(4)
        print(file_existence)
        if self.mode == "Normal":
            if 1 not in file_existence:
                with open(file_position + "\\" + input_keyword + "\\" + input_keyword + "_nml.txt", "w", encoding="utf-8")as f:
                    f.write("Accession number\tExperiment type\tRelease date\tTitle\tDescription\tArray\t"
                            "Protocol name\tProtocol description\tProtocol hardware\tPubMed ID\t")
                    label_list = ["Platform", "Cancer type", "Tumor location", "Tumor grade", "Histology", "Stage",
                                  "Survival event", "Survival time", "Primary", "Metastasis", "Therapy",
                                  "Radiation", "Response", "Sample info", "Organism", "Age", "Gender",
                                  "Ethnicity", "Smoking", "Pack years", "Alcohol", "Tissue", "Cell line",
                                  "Cell type", "Phenotype", "Genotype", "Treatment",
                                  "shRNA", "RNAi", "Pulldown", "Transfection", "Antibody", "Antibody vendor",
                                  "Antibody description", "Antibody target description"]
                    for i in label_list:
                        f.write(i + "\t")
                    f.write("other labels:\n")
                for acc in accs:
                    time.sleep(self.rest)
                    experiment_count = experiment_count + 1
                    print("start spider")
                    Main_spider.download(input_keyword, file_position, acc, extract_set)
                    time_left = int(
                        (time.time() - start_time) / experiment_count * (accession_numbers - experiment_count + 1))
                    progress = str(experiment_count) + " of " + str(accession_numbers) + " time left: " + str(time_left) + "seconds"
                    rate = int((experiment_count/accession_numbers) * 100)
                    self.signal.emit(progress, rate)
                    with open(file_position + "\\" + input_keyword + "\\accs\\" + input_keyword + "_accs_nml.txt", "a", encoding="utf-8")as f:
                        f.write(acc + "\t")
                end_time = time.time()
                last_time = int(end_time - start_time)
                progress = ("end. time used: %s seconds" % last_time)
                self.signal.emit(progress, 100)
            else:
                with open(file_position + "\\" + input_keyword + "\\accs\\" + input_keyword + "_accs_nml.txt", "r") as f:
                    old_list = f.read().split("\t")
                    old_list.pop(-1)
                    for i in old_list:
                        if i in accs:
                            accs.remove(i)
                accession_numbers = len(accs)
                if accs:
                    for acc in accs:
                        time.sleep(self.rest)
                        experiment_count = experiment_count + 1
                        print("start spider")
                        Main_spider.download(input_keyword, file_position, acc, extract_set)
                        time_left = int(
                            (time.time() - start_time) / experiment_count * (accession_numbers - experiment_count + 1))
                        progress = str(experiment_count) + " of " + str(accession_numbers) + " time left: " + str(time_left) + "seconds"
                        rate = int((experiment_count/accession_numbers) * 100)
                        self.signal.emit(progress, rate)
                        with open(file_position + "\\" + input_keyword + "\\accs\\" + input_keyword + "_accs_nml.txt", "a", encoding="utf-8")as f:
                            for i in accs:
                                f.write(i + "\t")
                    end_time = time.time()
                    last_time = int(end_time - start_time)
                    progress = ("end. time used: %s seconds" % last_time)
                    self.signal.emit(progress, 100)
                else:
                    progress = "no need to update"
                    self.signal.emit(progress, 100)
        elif self.mode == "Cell line focus":
            if 2 not in file_existence:
                with open(file_position + "\\" + input_keyword + "\\" + input_keyword + "_nml.txt", "w", encoding="utf-8")as f1:
                    with open(file_position + "\\" + input_keyword + "\\" + input_keyword + "_clf.txt", "w", encoding="utf-8")as f2:
                        f1.write("Accession number\tExperiment type\tRelease date\tTitle\tDescription\tArray\t"
                                "Protocol name\tProtocol description\tProtocol hardware\tPubMed ID\t")
                        f2.write("Accession number\tExperiment type\tRelease date\tTitle\tDescription\tArray\t"
                                "Protocol name\tProtocol description\tProtocol hardware\tPubMed ID\t")
                        label_list = ["Cancer type", "Tumor location", "Tumor grade", "Histology", "Stage",
                                      "Survival event", "Survival time", "Primary", "Metastasis", "Therapy",
                                      "Radiation", "Response", "Sample info", "Organism", "Age", "Gender",
                                      "Ethnicity", "Smoking", "Pack years", "Alcohol", "Tissue", "Cell line",
                                      "Cell type", "Tumor location", "Phenotype", "Genotype", "Treatment",
                                      "shRNA", "RNAi", "Pulldown", "Transfection", "Antibody", "Antibody vendor",
                                      "Antibody description", "Antibody target description"]
                        for i in label_list:
                            f1.write(i + "\t")
                            f2.write(i + "\t")
                        f1.write("other labels:\n")
                        f2.write("other labels:\n")
                for acc in accs:
                    time.sleep(self.rest)
                    experiment_count = experiment_count + 1
                    print("start spider")
                    Main_spider.download2(input_keyword, file_position, acc, extract_set)
                    time_left = int(
                        (time.time() - start_time) / experiment_count * (accession_numbers - experiment_count + 1))
                    progress = str(experiment_count) + " of " + str(accession_numbers) + " time left: " + str(time_left) + "seconds"
                    rate = int((experiment_count/accession_numbers) * 100)
                    self.signal.emit(progress, rate)
                    with open(file_position + "\\" + input_keyword + "\\accs\\" + input_keyword + "_accs_clf.txt", "a", encoding="utf-8")as f:
                        f.write(acc + "\t")
                end_time = time.time()
                last_time = int(end_time - start_time)
                progress = ("end. time used: %s seconds" % last_time)
                self.signal.emit(progress, 100)
            else:
                with open(file_position + "\\" + input_keyword + "\\accs\\" + input_keyword + "_accs_clf.txt", "r") as f:
                    old_list = f.read().split("\t")
                    old_list.pop(-1)
                    for i in old_list:
                        if i in accs:
                            accs.remove(i)
                accession_numbers = len(accs)
                if accs:
                    for acc in accs:
                        time.sleep(self.rest)
                        experiment_count = experiment_count + 1
                        print("start spider")
                        Main_spider.download2(input_keyword, file_position, acc, extract_set)
                        time_left = int(
                            (time.time() - start_time) / experiment_count * (accession_numbers - experiment_count + 1))
                        progress = str(experiment_count) + " of " + str(accession_numbers) + " time left: " + str(time_left) + "seconds"
                        rate = int((experiment_count/accession_numbers) * 100)
                        self.signal.emit(progress, rate)
                        with open(file_position + "\\" + input_keyword + "\\accs\\" + input_keyword + "_accs_clf.txt", "a", encoding="utf-8")as f:
                            for i in accs:
                                f.write(i + "\t")
                    end_time = time.time()
                    last_time = int(end_time - start_time)
                    progress = ("end. time used: %s seconds" % last_time)
                    self.signal.emit(progress, 100)
                else:
                    progress = "no need to update"
                    self.signal.emit(progress, 100)
        elif self.mode == "Not sorted":
            if 3 not in file_existence:
                for acc in accs:
                    time.sleep(self.rest)
                    experiment_count = experiment_count + 1
                    print("start spider")
                    Main_spider.download3(input_keyword, file_position, acc, extract_set)
                    time_left = int(
                        (time.time() - start_time) / experiment_count * (accession_numbers - experiment_count + 1))
                    progress = str(experiment_count) + " of " + str(accession_numbers) + " time left: " + str(time_left) + "seconds"
                    rate = int((experiment_count/accession_numbers) * 100)
                    self.signal.emit(progress, rate)
                    with open(file_position + "\\" + input_keyword + "\\accs\\" + input_keyword + "_accs_nst.txt", "a", encoding="utf-8")as f:
                        f.write(acc + "\t")
                end_time = time.time()
                last_time = int(end_time - start_time)
                progress = ("end. time used: %s seconds" % last_time)
                self.signal.emit(progress, 100)
            else:
                with open(file_position + "\\" + input_keyword + "\\accs\\" + input_keyword + "_accs_nst.txt", "r") as f:
                    old_list = f.read().split("\t")
                    old_list.pop(-1)
                    for i in old_list:
                        if i in accs:
                            accs.remove(i)
                accession_numbers = len(accs)
                if accs:
                    for acc in accs:
                        time.sleep(self.rest)
                        experiment_count = experiment_count + 1
                        print("start spider")
                        Main_spider.download3(input_keyword, file_position, acc, extract_set)
                        time_left = int(
                            (time.time() - start_time) / experiment_count * (accession_numbers - experiment_count + 1))
                        progress = str(experiment_count) + " of " + str(accession_numbers) + " time left: " + str(time_left) + "seconds"
                        rate = int((experiment_count/accession_numbers) * 100)
                        self.signal.emit(progress, rate)
                        with open(file_position + "\\" + input_keyword + "\\accs\\" + input_keyword + "_accs_nst.txt", "a", encoding="utf-8")as f:
                            for i in accs:
                                f.write(i + "\t")
                    end_time = time.time()
                    last_time = int(end_time - start_time)
                    progress = ("end. time used: %s seconds" % last_time)
                    self.signal.emit(progress, 100)
                else:
                    progress = "no need to update"
                    self.signal.emit(progress, 100)
        elif self.mode == "Raw":
            print("raw!")
            if 4 not in file_existence:
                for acc in accs:
                    time.sleep(self.rest)
                    experiment_count = experiment_count + 1
                    print("start spider")
                    Main_spider.download4(input_keyword, file_position, acc, extract_set)
                    time_left = int(
                        (time.time() - start_time) / experiment_count * (accession_numbers - experiment_count + 1))
                    progress = str(experiment_count) + " of " + str(accession_numbers) + " time left: " + str(time_left) + "seconds"
                    rate = int((experiment_count/accession_numbers) * 100)
                    self.signal.emit(progress, rate)
                    with open(file_position + "\\" + input_keyword + "\\accs\\" + input_keyword + "_accs_raw.txt", "a", encoding="utf-8")as f:
                        f.write(acc + "\t")
                end_time = time.time()
                last_time = int(end_time - start_time)
                progress = ("end. time used: %s seconds" % last_time)
                self.signal.emit(progress, 100)
            else:
                with open(file_position + "\\" + input_keyword + "\\accs\\" + input_keyword + "_accs_raw.txt", "r") as f:
                    old_list = f.read().split("\t")
                    old_list.pop(-1)
                    for i in old_list:
                        if i in accs:
                            accs.remove(i)
                accession_numbers = len(accs)
                if accs:
                    for acc in accs:
                        time.sleep(self.rest)
                        experiment_count = experiment_count + 1
                        print("start spider")
                        Main_spider.download4(input_keyword, file_position, acc, extract_set)
                        time_left = int(
                            (time.time() - start_time) / experiment_count * (accession_numbers - experiment_count + 1))
                        progress = str(experiment_count) + " of " + str(accession_numbers) + " time left: " + str(time_left) + "seconds"
                        rate = int((experiment_count/accession_numbers) * 100)
                        self.signal.emit(progress, rate)
                        with open(file_position + "\\" + input_keyword + "\\accs\\" + input_keyword + "_accs_raw.txt", "a", encoding="utf-8")as f:
                            for i in accs:
                                f.write(i + "\t")
                    end_time = time.time()
                    last_time = int(end_time - start_time)
                    progress = ("end. time used: %s seconds" % last_time)
                    self.signal.emit(progress, 100)
                else:
                    progress = "no need to update"
                    self.signal.emit(progress, 100)