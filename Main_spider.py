import requests
import re
from lxml import etree
import os


filter_list = [r"(platform)", r"(cancer type|disease.*stat|status|pathology|diagnose)", r"(location)", r"(grade|differentiation)",
               r"(histology|his\s|his$)", r"(stage|staging|tumor.*diagnosis|depth|t stage|pathological t|\[t\]|n stage|"
                                          r"pathological n|\[n\]|m stage|pathological m|\[m\]|tnm stage|tnm)",
               r"(death at|death due)", r"(death)", r"(primary)", r"(metasta)", r"(therapy|treated)", r"(radiation)",
               r"(response)", r"(sample.+|clinical.*information)", r"(organism)", r"(age)", r"(sex|gender)", r"(ethnicity)",
               r"(tobacco|smoking)", r"(pack years)", r"(alcohol)", r"(biomaterial|tissue)", r"(cell|strain)",
               r"(cell.*type)", r"(phenotype)", r"(genotype)", r"(treat)", r"(shrna)", r"(rna\s*i)",
               r"(pulldown)", r"(transfected|transfection)", r"antibody", r"(antibody.*vendor)", r"(antibody description)",
               r"(antibody.*target.*description)"]
label_list = ["Platform", "Cancer type", "Tumor location", "Tumor grade", "Histology", "Stage",
              "Survival event", "Survival time", "Primary", "Metastasis", "Therapy",
              "Radiation", "Response", "Sample info", "Organism", "Age", "Gender",
              "Ethnicity", "Smoking", "Pack years", "Alcohol", "Tissue", "Cell line",
              "Cell type", "Phenotype", "Genotype", "Treatment",
              "shRNA", "RNAi", "Pulldown", "Transfection", "Antibody", "Antibody vendor",
              "Antibody description", "Antibody target description"]
files_url = "https://www.ebi.ac.uk/arrayexpress/files/"
experiments_url = "https://www.ebi.ac.uk/arrayexpress/experiments/"
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0"}
dic_library = dict()
keys = list()
with open(os.getcwd() + "\\cell line library\\library.txt")as f:
    while True:
        temp = f.readline()
        if temp:
            a = temp.split("\t")[0]
            b = temp.split("\t")[2].strip("\n")
            try:
                if dic_library[a]:
                    dic_library[a].append(b)
            except KeyError:
                dic_library[a] = list()
                dic_library[a].append(b)
        else:
            break
for key in dic_library:
    keys.append(key)


def elem_filter(elem):
    filter_count = 0
    for i in filter_list:
        filter_count = filter_count + 1
        if re.search(i, elem, re.I):
            return filter_count


elem_list = []
elem_count = {}
experiment_count = 0
L = ["\t"] * 35

re_acc = re.compile(r"Comment.ArrayExpressAccession.\s+(.+\d+)(\s*|\n)")
re_date = re.compile(r"Public Release Date\s+(.+\d+)(\s*|\n)")
re_title = re.compile(r"Investigation Title\s+(.+)(\s*|\n)")
re_description = re.compile(r"Experiment Description\s+(.+)(\s*|\n)")
re_protocol_name = re.compile(r"Protocol Name\s+(.+)(\s*|\n)")
re_protocol_description = re.compile(r"Protocol Description\s+(.+)(\s*|\n)")
re_protocol_hardware = re.compile(r"Protocol Hardware\s+(.+)(\s*|\n)")
re_pmid = re.compile(r"pubmed.*?id.*?(\d+)", re.I)


def library_filter(site_primary, temp_check):
    for key in keys:
        if temp_check != "":
            if re.search(site_primary, key, re.I):
                for cell_line in dic_library[key]:
                    if re.match(temp_check, cell_line, re.I):
                        return True


def download(input_keyword, file_position, acc, extract_set):
    idf_url = files_url + acc + "/" + acc + ".idf.txt"
    sdrf_url = files_url + acc + "/" + acc + ".sdrf.txt"
    idf = requests.get(idf_url, headers=headers).text
    sdrf = requests.get(sdrf_url, headers=headers).text
    html = etree.HTML(requests.get(experiments_url + acc, headers=headers).text)
    files = html.xpath("//tbody//a/text()")
    divs = html.xpath("//td//div/text()")
    line0 = re.search(re_acc, idf).group(1).strip() + "\t"
    if line0:
        pass
    else:
        line0 = "\t"
    div_count = 0
    for div in divs:
        div_count = div_count + 1
        if re.match(r"experiment type.*", div, re.I):
            line1 = divs[div_count].strip() + "\t"
    if line1:
        pass
    else:
        line1 = "\t"
    if re.search(re_date, idf):
        line2 = re.search(re_date, idf).group(1).replace("\t", " ").strip() + "\t"
    else:
        line2 = "\t"
    if re.search(re_title, idf):
        line3 = re.search(re_title, idf).group(1).replace("\t", " ").strip() + "\t"
    else:
        line3 = "\t"
    if re.search(re_description, idf):
        line4 = re.search(re_description, idf).group(1).replace("\t", " ").strip() + "\t"
    else:
        line4 = "\t"
    line5 = ""
    for file in files:
        if re.match(r"(A-\w{4}-\d+).*", file):
            array = re.match(r"(A-\w{4}-\d+).*", file, re.I).group(1).replace("\t", " ").strip()
            array = array.split(" ")
            for a in array:
                temp = a + " https://www.ebi.ac.uk/arrayexpress/arrays/" + a
                line5 = line5 + temp
    if line5:
        line5 = line5 + "\t"
    else:
        line5 = "\t"
    if re.search(re_protocol_name, idf):
        line6 = re.search(re_protocol_name, idf).group(1).replace("\t", " ").strip() + "\t"
    else:
        line6 = "\t"
    if re.search(re_protocol_description, idf):
        line7 = re.search(re_protocol_description, idf).group(1).replace("\t", " ").strip() + "\t"
    else:
        line7 = "\t"
    if re.search(re_protocol_hardware, idf):
        line8 = re.search(re_protocol_hardware, idf).group(1).replace("\t", " ").strip() + "\t"
    else:
        line8 = "\t"
    if re.search(re_pmid, idf):
        line9 = re.search(re_pmid, idf).group(1).replace("\t", " ").strip() + "\t"
    else:
        line9 = "\t"
    basic_information = line0 + line1 + line2 + line3 + line4 + line5 + line6 + line7 + line8 + line9
    sdrf_lines = sdrf.split("\n")
    first_line = sdrf_lines[0]
    elems = first_line.split("\t")
    mark = -1
    marks = []
    unwanted_marks = []
    for elem in elems:
        mark = mark + 1
        if elem_filter(elem):
            marks.append(mark)
        else:
            unwanted_marks.append(mark)
    with open(file_position + "\\" + input_keyword + "\\" + input_keyword + "_nml.txt", "a", encoding="utf-8") as f:
        for lines in sdrf_lines[1:-1]:
            L1 = L[::]
            line = lines.split("\t")
            for i in marks:
                L1[elem_filter(elems[i]) - 1] = line[i].strip() + "\t"
            checking_place = L1[1] + L1[2] + L1[13] + L1[14] + L1[21] + L1[22] + L1[23]
            unwanted = ""
            for i in unwanted_marks:
                unwanted = line[i] + unwanted
            checking_place = checking_place + unwanted
            checking_place2 = L1[22]
            checking_place2 = re.split(r"\W+", checking_place2)
            temp_check = ""
            for i in checking_place2:
                temp_check = temp_check + i
                temp_check = temp_check.replace("_", "")
            checking_state = 0
            for i in extract_set:
                if (re.search(i, checking_place, re.I) or library_filter(i, temp_check))and checking_state == 0:
                    checking_state = 1
                    f.write(basic_information)
                    for i in L1:
                        f.write(i)
                    for i in unwanted_marks:
                        f.write(elems[i] + ": " + line[i] + "; ")
                    f.write("\n")
                else:
                    pass


def download2(input_keyword, file_position, acc, extract_set):
    idf_url = files_url + acc + "/" + acc + ".idf.txt"
    sdrf_url = files_url + acc + "/" + acc + ".sdrf.txt"
    idf = requests.get(idf_url, headers=headers).text
    sdrf = requests.get(sdrf_url, headers=headers).text
    html = etree.HTML(requests.get(experiments_url + acc, headers=headers).text)
    files = html.xpath("//tbody//a/text()")
    divs = html.xpath("//td//div/text()")
    line0 = re.search(re_acc, idf).group(1).strip() + "\t"
    if line0:
        pass
    else:
        line0 = "\t"
    div_count = 0
    for div in divs:
        div_count = div_count + 1
        if re.match(r"experiment type.*", div, re.I):
            line1 = divs[div_count].strip() + "\t"
    if line1:
        pass
    else:
        line1 = "\t"
    if re.search(re_date, idf):
        line2 = re.search(re_date, idf).group(1).replace("\t", " ").strip() + "\t"
    else:
        line2 = "\t"
    if re.search(re_title, idf):
        line3 = re.search(re_title, idf).group(1).replace("\t", " ").strip() + "\t"
    else:
        line3 = "\t"
    if re.search(re_description, idf):
        line4 = re.search(re_description, idf).group(1).replace("\t", " ").strip() + "\t"
    else:
        line4 = "\t"
    line5 = ""
    for file in files:
        if re.match(r"(A-\w{4}-\d+).*", file):
            array = re.match(r"(A-\w{4}-\d+).*", file, re.I).group(1).replace("\t", " ").strip()
            array = array.split(" ")
            for a in array:
                temp = a + " https://www.ebi.ac.uk/arrayexpress/arrays/" + a
                line5 = line5 + temp
    if line5:
        line5 = line5 + "\t"
    else:
        line5 = "\t"
    if re.search(re_protocol_name, idf):
        line6 = re.search(re_protocol_name, idf).group(1).replace("\t", " ").strip() + "\t"
    else:
        line6 = "\t"
    if re.search(re_protocol_description, idf):
        line7 = re.search(re_protocol_description, idf).group(1).replace("\t", " ").strip() + "\t"
    else:
        line7 = "\t"
    if re.search(re_protocol_hardware, idf):
        line8 = re.search(re_protocol_hardware, idf).group(1).replace("\t", " ").strip() + "\t"
    else:
        line8 = "\t"
    if re.search(re_pmid, idf):
        line9 = re.search(re_pmid, idf).group(1).replace("\t", " ").strip() + "\t"
    else:
        line9 = "\t"
    basic_information = line0 + line1 + line2 + line3 + line4 + line5 + line6 + line7 + line8 + line9
    sdrf_lines = sdrf.split("\n")
    first_line = sdrf_lines[0]
    elems = first_line.split("\t")
    mark = -1
    marks = []
    unwanted_marks = []
    for elem in elems:
        mark = mark + 1
        if elem_filter(elem):
            marks.append(mark)
        else:
            unwanted_marks.append(mark)
    with open(file_position + "\\" + input_keyword + "\\" + input_keyword + "_nml.txt", "a", encoding="utf-8") as f1:
        with open(file_position + "\\" + input_keyword + "\\" + input_keyword + "_clf.txt", "a", encoding="utf-8") as f2:
            for lines in sdrf_lines[1:-1]:
                L1 = L[::]
                line = lines.split("\t")
                for i in marks:
                    L1[elem_filter(elems[i]) - 1] = line[i].strip() + "\t"
                checking_place = L1[1] + L1[2] + L1[13] + L1[14] + L1[21] + L1[22] + L1[23]
                unwanted = ""
                for i in unwanted_marks:
                    unwanted = line[i] + unwanted
                checking_place = checking_place + unwanted
                checking_place2 = L1[22]
                checking_place2 = re.split(r"\W+", checking_place2)
                temp_check = ""
                for i in checking_place2:
                    temp_check = temp_check + i
                    temp_check = temp_check.replace("_", "")
                checking_state = 0
                for i in extract_set:
                    if library_filter(i, temp_check) and checking_state == 0:
                        checking_state = 1
                        f1.write(basic_information)
                        f2.write(basic_information)
                        for i in L1:
                            f1.write(i)
                            f2.write(i)
                        for i in unwanted_marks:
                            f1.write(elems[i] + ": " + line[i] + "; ")
                            f2.write(elems[i] + ": " + line[i] + "; ")
                        f1.write("\n")
                        f2.write("\n")
                    elif re.search(i, checking_place, re.I)and checking_state == 0:
                        checking_state = 1
                        f1.write(basic_information)
                        for i in L1:
                            f1.write(i)
                        for i in unwanted_marks:
                            f1.write(elems[i] + ": " + line[i] + "; ")
                        f1.write("\n")
                    else:
                        pass


def download3(input_keyword, file_position, acc, extract_set):
    sdrf_url = files_url + acc + "/" + acc + ".sdrf.txt"
    sdrf = requests.get(sdrf_url, headers=headers).text
    sdrf_lines = sdrf.split("\n")
    first_line = sdrf_lines[0]
    with open(file_position + "\\" + input_keyword + "\\" + input_keyword + "_nst.txt", "a", encoding="utf-8") as f:
        f.write(first_line)
        for lines in sdrf_lines[1:-1]:
            line = lines.split("\t")
            checking_place = ""
            for i in line:
                checking_place += i
            checking_state = 0
            for i in extract_set:
                if re.search(i, checking_place, re.I)and checking_state == 0:
                    checking_state = 1
                    f.write(lines)
                    f.write("\n")
                else:
                    pass


def download4(input_keyword, file_position, acc, extract_set):
    sdrf_url = files_url + acc + "/" + acc + ".sdrf.txt"
    sdrf = requests.get(sdrf_url, headers=headers).text
    sdrf_lines = sdrf.split("\n")
    with open(file_position + "\\" + input_keyword + "\\" + input_keyword + "_raw.txt", "a", encoding="utf-8") as f:
        for lines in sdrf_lines:
            f.write(lines)
            f.write("\n")
