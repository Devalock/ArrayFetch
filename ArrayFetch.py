from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog
import fetch_thread
import download_files
import sqlite3
import xlwt
import os
input_keyword = ""
file_name = ""
file_position = ""
mode = ""
download_set = set()
parameters = []
a = "cancer_type,tumor_location,tumor_grade,histology,stage,survival_event,survival_time,pri_mary,metastasis,therapy," \
    "radiation,response,sample_info,organism,age,gender,ethnicity,smoking,pack_years,alcohol,tissue,cell_line," \
    "cell_type,phenotype,genotype,treatment,shrna,rnai,pulldown,transfection,antibody,antibody_vendor," \
    "antibody_description,antibody_target_description,other_labels"
gather_list = []
db_library = {}
count = 0
for i in a.split(","):
    count += 1
    db_library[count] = i
for i in range(1, 36):
    gather_list.append(i)


class Ui_ArrayFetch(QtWidgets.QWidget):
    try:
        global file_position
        with open(os.getcwd() + "\\default file position\\default.txt", "r", encoding="utf-8") as f:
            file_position = f.read()
    except IOError:
        pass

    try:
        global parameters
        with open(os.getcwd() + "\\parameters\\parameters.txt", "r", encoding="utf-8") as f:
            param = f.read().split("\n")
            for i in param:
                if i:
                    parameters.append(int(i))
    except IOError:
        parameters = [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
                      2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
                      2, 2, 2, 2]

    def choose_dir(self):
        global file_position
        file_position = QFileDialog.getExistingDirectory(self, "choose a directory", file_position)

    def set_dir(self):
        _translate = QtCore.QCoreApplication.translate
        self.file_position.setText(_translate("Dialog", file_position))

    def choose_file(self):
        global file_name
        file_name = QFileDialog.getOpenFileName(self, "choose a file",  file_position, "Text Files (*.txt)")[0]

    def open_file(self):
        self.tableWidget.setRowCount(0)
        if file_name:
            with open(file_name, "r", encoding="utf-8") as f:
                while True:
                    row_count = self.tableWidget.rowCount()
                    self.tableWidget.insertRow(row_count)
                    line = f.readline().split("\t")
                    if len(line) != 1:
                        count = -1
                        for i in line:
                            count = count + 1
                            self.tableWidget.setItem(row_count, count, QtWidgets.QTableWidgetItem(str(i)))
                    else:
                        break

    def get_keyword(self):
        global input_keyword
        if self.input_keywords.text():
            input_keyword = self.input_keywords.text()

    def set_requires(self):
        if file_position and input_keyword:
            if os.path.exists(file_position + "\\" + input_keyword):
                pass
            else:
                os.mkdir(file_position + "\\" + input_keyword)
        if file_position and input_keyword:
            fetch_thread.set_requires(input_keyword, file_position)
        else:
            self.progress.setText("please check your directory or keyword!")

    def set_downloads(self):
        if download_set and file_position:
            download_files.set_download(download_set, file_position, input_keyword)
        else:
            self.progress_2.setText("please check your directory or keyword!")

    def setupUi(self, ArrayFetch):
        ArrayFetch.setObjectName("ArrayFetch")
        ArrayFetch.resize(1233, 836)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        ArrayFetch.setFont(font)
        self.centralwidget = QtWidgets.QWidget(ArrayFetch)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setWhatsThis("")
        self.groupBox.setObjectName("groupBox")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName("gridLayout")
        self.file_position = QtWidgets.QLineEdit(self.groupBox)
        self.file_position.setText(file_position)
        self.file_position.setObjectName("file_position")
        self.gridLayout.addWidget(self.file_position, 0, 1, 1, 7)
        self.input_keywords = QtWidgets.QLineEdit(self.groupBox)
        self.input_keywords.setWhatsThis("")
        self.input_keywords.setInputMask("")
        self.input_keywords.setText("")
        self.input_keywords.setObjectName("input_keywords")
        self.gridLayout.addWidget(self.input_keywords, 1, 0, 1, 7)
        self.progressBar = QtWidgets.QProgressBar(self.groupBox)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.gridLayout.addWidget(self.progressBar, 2, 0, 1, 8)
        self.progress = QtWidgets.QLabel(self.groupBox)
        self.progress.setObjectName("progress")
        self.gridLayout.addWidget(self.progress, 4, 0, 1, 3)
        self.spinBox = QtWidgets.QSpinBox(self.groupBox)
        self.spinBox.setMinimum(6)
        self.spinBox.setMaximum(18)
        self.spinBox.setObjectName("spinBox")
        self.gridLayout.addWidget(self.spinBox, 4, 7, 1, 1)
        self.search_btn = QtWidgets.QPushButton(self.groupBox)
        self.search_btn.setMaximumSize(QtCore.QSize(93, 16777215))
        self.search_btn.setObjectName("search_btn")
        self.gridLayout.addWidget(self.search_btn, 1, 7, 1, 1)
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 4, 6, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 4, 4, 1, 1)
        self.set_file_position_btn = QtWidgets.QPushButton(self.groupBox)
        self.set_file_position_btn.setMaximumSize(QtCore.QSize(107, 16777215))
        self.set_file_position_btn.setObjectName("set_file_position_btn")
        self.gridLayout.addWidget(self.set_file_position_btn, 0, 0, 1, 1)
        self.comboBox = QtWidgets.QComboBox(self.groupBox)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.gridLayout.addWidget(self.comboBox, 4, 5, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 4, 3, 1, 1)
        self.gridLayout_2.addWidget(self.groupBox, 0, 0, 1, 1)
        self.groupBox_2 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_2.setTitle("")
        self.groupBox_2.setObjectName("groupBox_2")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.groupBox_2)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.excel = QtWidgets.QPushButton(self.groupBox_2)
        self.excel.setMaximumSize(QtCore.QSize(146, 16777215))
        self.excel.setObjectName("excel")
        self.gridLayout_3.addWidget(self.excel, 1, 3, 1, 1)
        self.plainTextEdit = QtWidgets.QPlainTextEdit(self.groupBox_2)
        self.plainTextEdit.setMaximumSize(QtCore.QSize(16777215, 87))
        self.plainTextEdit.setPlainText("")
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.gridLayout_3.addWidget(self.plainTextEdit, 4, 0, 1, 5)
        self.open_file_btn = QtWidgets.QPushButton(self.groupBox_2)
        self.open_file_btn.setMaximumSize(QtCore.QSize(93, 16777215))
        self.open_file_btn.setObjectName("open_file_btn")
        self.gridLayout_3.addWidget(self.open_file_btn, 1, 0, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem1, 1, 2, 1, 1)
        self.tableWidget = QtWidgets.QTableWidget(self.groupBox_2)
        self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(46)
        self.tableWidget.setRowCount(0)
        self.tableWidget.setHorizontalHeaderLabels(['Accession number', 'Experiment type', 'Release date', 'Title',
                                                    'Description', 'Array', 'Protocol name', 'Protocol description',
                                                    'Protocol hardware', 'PubMed ID', 'Platform', 'Cancer type',
                                                    'Tumor location', 'Tumor grade', 'Histology', 'Stage',
                                                    'Survival event', 'Survival time', 'Primary', 'Metastasis',
                                                    'Therapy', 'Radiation', 'Response', 'Sample info', 'Organism',
                                                    'Age', 'Gender', 'Ethnicity', 'Smoking', 'Pack years', 'Alcohol',
                                                    'Tissue', 'Cell line', 'Cell type', 'Phenotype', 'Genotype',
                                                    'Treatment', 'shRNA', 'RNAi', 'Pulldown', 'Transfection',
                                                    'Antibody', 'Antibody vendor', 'Antibody description',
                                                    'Antibody target description', 'other labels:'])
        self.tableWidget.setColumnWidth(0, 150)
        self.tableWidget.setColumnWidth(1, 150)
        self.tableWidget.setColumnWidth(7, 180)
        self.tableWidget.setColumnWidth(8, 170)
        self.tableWidget.setColumnWidth(42, 170)
        self.tableWidget.setColumnWidth(43, 170)
        self.tableWidget.setColumnWidth(44, 250)
        self.gridLayout_3.addWidget(self.tableWidget, 3, 0, 1, 5)
        self.plainTextEdit_2 = QtWidgets.QPlainTextEdit(self.groupBox_2)
        self.plainTextEdit_2.setMaximumSize(QtCore.QSize(128, 16777215))
        self.plainTextEdit_2.setPlainText("")
        self.plainTextEdit_2.setObjectName("plainTextEdit_2")
        self.gridLayout_3.addWidget(self.plainTextEdit_2, 3, 5, 2, 1)
        self.download = QtWidgets.QPushButton(self.groupBox_2)
        self.download.setObjectName("download")
        self.gridLayout_3.addWidget(self.download, 1, 5, 1, 1)
        self.progressBar_2 = QtWidgets.QProgressBar(self.groupBox_2)
        self.progressBar_2.setMaximumSize(QtCore.QSize(450, 16777215))
        self.progressBar_2.setProperty("value", 0)
        self.progressBar_2.setObjectName("progressBar_2")
        self.gridLayout_3.addWidget(self.progressBar_2, 5, 2, 1, 4)
        self.tabWidget = QtWidgets.QTabWidget(self.groupBox_2)
        self.tabWidget.setMaximumSize(QtCore.QSize(540, 16777215))
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.tab)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.Age_1 = QtWidgets.QCheckBox(self.tab)
        self.Age_1.setChecked(True)
        self.Age_1.setObjectName("Age_1")
        self.gridLayout_4.addWidget(self.Age_1, 4, 1, 1, 1)
        self.Histology_1 = QtWidgets.QCheckBox(self.tab)
        self.Histology_1.setChecked(True)
        self.Histology_1.setObjectName("Histology_1")
        self.gridLayout_4.addWidget(self.Histology_1, 5, 0, 1, 1)
        self.Cancer_type_1 = QtWidgets.QCheckBox(self.tab)
        self.Cancer_type_1.setChecked(True)
        self.Cancer_type_1.setObjectName("Cancer_type_1")
        self.gridLayout_4.addWidget(self.Cancer_type_1, 2, 0, 1, 1)
        self.shRNA_1 = QtWidgets.QCheckBox(self.tab)
        self.shRNA_1.setChecked(True)
        self.shRNA_1.setObjectName("shRNA_1")
        self.gridLayout_4.addWidget(self.shRNA_1, 3, 2, 1, 1)
        self.Gender_1 = QtWidgets.QCheckBox(self.tab)
        self.Gender_1.setChecked(True)
        self.Gender_1.setObjectName("Gender_1")
        self.gridLayout_4.addWidget(self.Gender_1, 5, 1, 1, 1)
        self.RNAi_1 = QtWidgets.QCheckBox(self.tab)
        self.RNAi_1.setChecked(True)
        self.RNAi_1.setObjectName("RNAi_1")
        self.gridLayout_4.addWidget(self.RNAi_1, 4, 2, 1, 1)
        self.Tumor_grade_1 = QtWidgets.QCheckBox(self.tab)
        self.Tumor_grade_1.setChecked(True)
        self.Tumor_grade_1.setObjectName("Tumor_grade_1")
        self.gridLayout_4.addWidget(self.Tumor_grade_1, 4, 0, 1, 1)
        self.Pulldown_1 = QtWidgets.QCheckBox(self.tab)
        self.Pulldown_1.setChecked(True)
        self.Pulldown_1.setObjectName("Pulldown_1")
        self.gridLayout_4.addWidget(self.Pulldown_1, 5, 2, 1, 1)
        self.reverse_1 = QtWidgets.QPushButton(self.tab)
        self.reverse_1.setMinimumSize(QtCore.QSize(140, 0))
        self.reverse_1.setMaximumSize(QtCore.QSize(140, 16777215))
        self.reverse_1.setObjectName("reverse_1")
        self.gridLayout_4.addWidget(self.reverse_1, 0, 2, 1, 1)
        self.Treatment_1 = QtWidgets.QCheckBox(self.tab)
        self.Treatment_1.setChecked(True)
        self.Treatment_1.setObjectName("Treatment_1")
        self.gridLayout_4.addWidget(self.Treatment_1, 2, 2, 1, 1)
        self.Stage_1 = QtWidgets.QCheckBox(self.tab)
        self.Stage_1.setChecked(True)
        self.Stage_1.setObjectName("Stage_1")
        self.gridLayout_4.addWidget(self.Stage_1, 6, 0, 1, 1)
        self.Tumor_location_1 = QtWidgets.QCheckBox(self.tab)
        self.Tumor_location_1.setChecked(True)
        self.Tumor_location_1.setObjectName("Tumor_location_1")
        self.gridLayout_4.addWidget(self.Tumor_location_1, 3, 0, 1, 1)
        self.Ethnicity_1 = QtWidgets.QCheckBox(self.tab)
        self.Ethnicity_1.setChecked(True)
        self.Ethnicity_1.setObjectName("Ethnicity_1")
        self.gridLayout_4.addWidget(self.Ethnicity_1, 6, 1, 1, 1)
        self.Transfection_1 = QtWidgets.QCheckBox(self.tab)
        self.Transfection_1.setChecked(True)
        self.Transfection_1.setObjectName("Transfection_1")
        self.gridLayout_4.addWidget(self.Transfection_1, 6, 2, 1, 1)
        self.cancel_all_1 = QtWidgets.QPushButton(self.tab)
        self.cancel_all_1.setMinimumSize(QtCore.QSize(140, 0))
        self.cancel_all_1.setMaximumSize(QtCore.QSize(140, 16777215))
        self.cancel_all_1.setObjectName("cancel_all_1")
        self.gridLayout_4.addWidget(self.cancel_all_1, 0, 1, 1, 1)
        self.Sample_info_1 = QtWidgets.QCheckBox(self.tab)
        self.Sample_info_1.setChecked(True)
        self.Sample_info_1.setObjectName("Sample_info_1")
        self.gridLayout_4.addWidget(self.Sample_info_1, 2, 1, 1, 1)
        self.Organism_1 = QtWidgets.QCheckBox(self.tab)
        self.Organism_1.setChecked(True)
        self.Organism_1.setObjectName("Organism_1")
        self.gridLayout_4.addWidget(self.Organism_1, 3, 1, 1, 1)
        self.select_all_1 = QtWidgets.QPushButton(self.tab)
        self.select_all_1.setMinimumSize(QtCore.QSize(140, 0))
        self.select_all_1.setMaximumSize(QtCore.QSize(140, 16777215))
        self.select_all_1.setObjectName("select_all_1")
        self.gridLayout_4.addWidget(self.select_all_1, 0, 0, 1, 1)
        self.Alcohol_1 = QtWidgets.QCheckBox(self.tab)
        self.Alcohol_1.setChecked(True)
        self.Alcohol_1.setObjectName("Alcohol_1")
        self.gridLayout_4.addWidget(self.Alcohol_1, 9, 1, 1, 1)
        self.Smoking_1 = QtWidgets.QCheckBox(self.tab)
        self.Smoking_1.setChecked(True)
        self.Smoking_1.setObjectName("Smoking_1")
        self.gridLayout_4.addWidget(self.Smoking_1, 7, 1, 1, 1)
        self.Antibody_vendor_1 = QtWidgets.QCheckBox(self.tab)
        self.Antibody_vendor_1.setChecked(True)
        self.Antibody_vendor_1.setObjectName("Antibody_vendor_1")
        self.gridLayout_4.addWidget(self.Antibody_vendor_1, 8, 2, 2, 1)
        self.Tissue_1 = QtWidgets.QCheckBox(self.tab)
        self.Tissue_1.setChecked(True)
        self.Tissue_1.setObjectName("Tissue_1")
        self.gridLayout_4.addWidget(self.Tissue_1, 10, 1, 1, 1)
        self.Antibody_description_1 = QtWidgets.QCheckBox(self.tab)
        self.Antibody_description_1.setChecked(True)
        self.Antibody_description_1.setObjectName("Antibody_description_1")
        self.gridLayout_4.addWidget(self.Antibody_description_1, 10, 2, 2, 1)
        self.Cell_line_1 = QtWidgets.QCheckBox(self.tab)
        self.Cell_line_1.setChecked(True)
        self.Cell_line_1.setObjectName("Cell_line_1")
        self.gridLayout_4.addWidget(self.Cell_line_1, 11, 1, 1, 1)
        self.Antibody_1 = QtWidgets.QCheckBox(self.tab)
        self.Antibody_1.setChecked(True)
        self.Antibody_1.setObjectName("Antibody_1")
        self.gridLayout_4.addWidget(self.Antibody_1, 7, 2, 1, 1)
        self.Pack_years_1 = QtWidgets.QCheckBox(self.tab)
        self.Pack_years_1.setChecked(True)
        self.Pack_years_1.setObjectName("Pack_years_1")
        self.gridLayout_4.addWidget(self.Pack_years_1, 8, 1, 1, 1)
        self.Phenotype_1 = QtWidgets.QCheckBox(self.tab)
        self.Phenotype_1.setChecked(True)
        self.Phenotype_1.setObjectName("Phenotype_1")
        self.gridLayout_4.addWidget(self.Phenotype_1, 13, 1, 1, 1)
        self.Antibody_target_description_1 = QtWidgets.QCheckBox(self.tab)
        self.Antibody_target_description_1.setChecked(True)
        self.Antibody_target_description_1.setObjectName("Antibody_target_description_1")
        self.gridLayout_4.addWidget(self.Antibody_target_description_1, 12, 2, 2, 1)
        self.Cell_type_1 = QtWidgets.QCheckBox(self.tab)
        self.Cell_type_1.setChecked(True)
        self.Cell_type_1.setObjectName("Cell_type_1")
        self.gridLayout_4.addWidget(self.Cell_type_1, 12, 1, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.tab)
        self.label_4.setMaximumSize(QtCore.QSize(16777215, 30))
        self.label_4.setObjectName("label_4")
        self.gridLayout_4.addWidget(self.label_4, 1, 1, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.tab)
        self.label_5.setMaximumSize(QtCore.QSize(16777215, 30))
        self.label_5.setObjectName("label_5")
        self.gridLayout_4.addWidget(self.label_5, 1, 2, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.tab)
        self.label_3.setMaximumSize(QtCore.QSize(16777215, 30))
        self.label_3.setObjectName("label_3")
        self.gridLayout_4.addWidget(self.label_3, 1, 0, 1, 1)
        self.Genotype_1 = QtWidgets.QCheckBox(self.tab)
        self.Genotype_1.setChecked(True)
        self.Genotype_1.setObjectName("Genotype_1")
        self.gridLayout_4.addWidget(self.Genotype_1, 14, 1, 1, 1)
        self.Other_labels_1 = QtWidgets.QCheckBox(self.tab)
        self.Other_labels_1.setChecked(True)
        self.Other_labels_1.setObjectName("Other_labels_1")
        self.gridLayout_4.addWidget(self.Other_labels_1, 14, 2, 1, 1)
        self.Survival_event_1 = QtWidgets.QCheckBox(self.tab)
        self.Survival_event_1.setChecked(True)
        self.Survival_event_1.setObjectName("Survival_event_1")
        self.gridLayout_4.addWidget(self.Survival_event_1, 7, 0, 1, 1)
        self.Survival_time_1 = QtWidgets.QCheckBox(self.tab)
        self.Survival_time_1.setChecked(True)
        self.Survival_time_1.setObjectName("Survival_time_1")
        self.gridLayout_4.addWidget(self.Survival_time_1, 8, 0, 1, 1)
        self.Primary_1 = QtWidgets.QCheckBox(self.tab)
        self.Primary_1.setChecked(True)
        self.Primary_1.setObjectName("Primary_1")
        self.gridLayout_4.addWidget(self.Primary_1, 9, 0, 1, 1)
        self.Metastasis_1 = QtWidgets.QCheckBox(self.tab)
        self.Metastasis_1.setChecked(True)
        self.Metastasis_1.setObjectName("Metastasis_1")
        self.gridLayout_4.addWidget(self.Metastasis_1, 10, 0, 1, 1)
        self.Therapy_1 = QtWidgets.QCheckBox(self.tab)
        self.Therapy_1.setChecked(True)
        self.Therapy_1.setObjectName("Therapy_1")
        self.gridLayout_4.addWidget(self.Therapy_1, 11, 0, 1, 1)
        self.Radiation_1 = QtWidgets.QCheckBox(self.tab)
        self.Radiation_1.setChecked(True)
        self.Radiation_1.setObjectName("Radiation_1")
        self.gridLayout_4.addWidget(self.Radiation_1, 12, 0, 1, 1)
        self.Response_1 = QtWidgets.QCheckBox(self.tab)
        self.Response_1.setChecked(True)
        self.Response_1.setObjectName("Response_1")
        self.gridLayout_4.addWidget(self.Response_1, 13, 0, 1, 1)
        self.tabWidget.addTab(self.tab, "")
        self.tab_4 = QtWidgets.QWidget()
        self.tab_4.setObjectName("tab_4")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.tab_4)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.select_all_2 = QtWidgets.QPushButton(self.tab_4)
        self.select_all_2.setMinimumSize(QtCore.QSize(140, 0))
        self.select_all_2.setMaximumSize(QtCore.QSize(140, 16777215))
        self.select_all_2.setObjectName("select_all_2")
        self.gridLayout_5.addWidget(self.select_all_2, 0, 0, 1, 1)
        self.label_7 = QtWidgets.QLabel(self.tab_4)
        self.label_7.setMaximumSize(QtCore.QSize(16777215, 30))
        self.label_7.setObjectName("label_7")
        self.gridLayout_5.addWidget(self.label_7, 2, 1, 1, 1)
        self.label_9 = QtWidgets.QLabel(self.tab_4)
        self.label_9.setMaximumSize(QtCore.QSize(16777215, 30))
        self.label_9.setObjectName("label_9")
        self.gridLayout_5.addWidget(self.label_9, 2, 2, 1, 1)
        self.Treatment_2 = QtWidgets.QCheckBox(self.tab_4)
        self.Treatment_2.setChecked(True)
        self.Treatment_2.setObjectName("Treatment_2")
        self.gridLayout_5.addWidget(self.Treatment_2, 3, 2, 1, 1)
        self.reverse_2 = QtWidgets.QPushButton(self.tab_4)
        self.reverse_2.setMaximumSize(QtCore.QSize(140, 16777215))
        self.reverse_2.setObjectName("reverse_2")
        self.gridLayout_5.addWidget(self.reverse_2, 0, 2, 1, 1)
        self.Tumor_location_2 = QtWidgets.QCheckBox(self.tab_4)
        self.Tumor_location_2.setChecked(True)
        self.Tumor_location_2.setObjectName("Tumor_location_2")
        self.gridLayout_5.addWidget(self.Tumor_location_2, 4, 0, 1, 1)
        self.cancel_all_2 = QtWidgets.QPushButton(self.tab_4)
        self.cancel_all_2.setMinimumSize(QtCore.QSize(140, 0))
        self.cancel_all_2.setMaximumSize(QtCore.QSize(140, 16777215))
        self.cancel_all_2.setObjectName("cancel_all_2")
        self.gridLayout_5.addWidget(self.cancel_all_2, 0, 1, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.tab_4)
        self.label_6.setMaximumSize(QtCore.QSize(16777215, 30))
        self.label_6.setObjectName("label_6")
        self.gridLayout_5.addWidget(self.label_6, 2, 0, 1, 1)
        self.Sample_info_2 = QtWidgets.QCheckBox(self.tab_4)
        self.Sample_info_2.setChecked(True)
        self.Sample_info_2.setObjectName("Sample_info_2")
        self.gridLayout_5.addWidget(self.Sample_info_2, 3, 1, 1, 1)
        self.Organism_2 = QtWidgets.QCheckBox(self.tab_4)
        self.Organism_2.setChecked(True)
        self.Organism_2.setObjectName("Organism_2")
        self.gridLayout_5.addWidget(self.Organism_2, 4, 1, 1, 1)
        self.Cancer_type_2 = QtWidgets.QCheckBox(self.tab_4)
        self.Cancer_type_2.setChecked(True)
        self.Cancer_type_2.setObjectName("Cancer_type_2")
        self.gridLayout_5.addWidget(self.Cancer_type_2, 3, 0, 1, 1)
        self.Pulldown_2 = QtWidgets.QCheckBox(self.tab_4)
        self.Pulldown_2.setChecked(True)
        self.Pulldown_2.setObjectName("Pulldown_2")
        self.gridLayout_5.addWidget(self.Pulldown_2, 6, 2, 1, 1)
        self.Stage_2 = QtWidgets.QCheckBox(self.tab_4)
        self.Stage_2.setChecked(True)
        self.Stage_2.setObjectName("Stage_2")
        self.gridLayout_5.addWidget(self.Stage_2, 7, 0, 1, 1)
        self.Tumor_grade_2 = QtWidgets.QCheckBox(self.tab_4)
        self.Tumor_grade_2.setChecked(True)
        self.Tumor_grade_2.setObjectName("Tumor_grade_2")
        self.gridLayout_5.addWidget(self.Tumor_grade_2, 5, 0, 1, 1)
        self.Gender_2 = QtWidgets.QCheckBox(self.tab_4)
        self.Gender_2.setChecked(True)
        self.Gender_2.setObjectName("Gender_2")
        self.gridLayout_5.addWidget(self.Gender_2, 6, 1, 1, 1)
        self.shRNA_2 = QtWidgets.QCheckBox(self.tab_4)
        self.shRNA_2.setChecked(True)
        self.shRNA_2.setObjectName("shRNA_2")
        self.gridLayout_5.addWidget(self.shRNA_2, 4, 2, 1, 1)
        self.RNAi_2 = QtWidgets.QCheckBox(self.tab_4)
        self.RNAi_2.setChecked(True)
        self.RNAi_2.setObjectName("RNAi_2")
        self.gridLayout_5.addWidget(self.RNAi_2, 5, 2, 1, 1)
        self.Age_2 = QtWidgets.QCheckBox(self.tab_4)
        self.Age_2.setChecked(True)
        self.Age_2.setObjectName("Age_2")
        self.gridLayout_5.addWidget(self.Age_2, 5, 1, 1, 1)
        self.Histology_2 = QtWidgets.QCheckBox(self.tab_4)
        self.Histology_2.setChecked(True)
        self.Histology_2.setObjectName("Histology_2")
        self.gridLayout_5.addWidget(self.Histology_2, 6, 0, 1, 1)
        self.Ethnicity_2 = QtWidgets.QCheckBox(self.tab_4)
        self.Ethnicity_2.setChecked(True)
        self.Ethnicity_2.setObjectName("Ethnicity_2")
        self.gridLayout_5.addWidget(self.Ethnicity_2, 7, 1, 1, 1)
        self.Transfection_2 = QtWidgets.QCheckBox(self.tab_4)
        self.Transfection_2.setChecked(True)
        self.Transfection_2.setObjectName("Transfection_2")
        self.gridLayout_5.addWidget(self.Transfection_2, 7, 2, 1, 1)
        self.Pack_years_2 = QtWidgets.QCheckBox(self.tab_4)
        self.Pack_years_2.setChecked(True)
        self.Pack_years_2.setObjectName("Pack_years_2")
        self.gridLayout_5.addWidget(self.Pack_years_2, 9, 1, 1, 1)
        self.Antibody_vendor_2 = QtWidgets.QCheckBox(self.tab_4)
        self.Antibody_vendor_2.setChecked(True)
        self.Antibody_vendor_2.setObjectName("Antibody_vendor_2")
        self.gridLayout_5.addWidget(self.Antibody_vendor_2, 9, 2, 2, 1)
        self.Tissue_2 = QtWidgets.QCheckBox(self.tab_4)
        self.Tissue_2.setChecked(True)
        self.Tissue_2.setObjectName("Tissue_2")
        self.gridLayout_5.addWidget(self.Tissue_2, 11, 1, 1, 1)
        self.Alcohol_2 = QtWidgets.QCheckBox(self.tab_4)
        self.Alcohol_2.setChecked(True)
        self.Alcohol_2.setObjectName("Alcohol_2")
        self.gridLayout_5.addWidget(self.Alcohol_2, 10, 1, 1, 1)
        self.Antibody_2 = QtWidgets.QCheckBox(self.tab_4)
        self.Antibody_2.setChecked(True)
        self.Antibody_2.setObjectName("Antibody_2")
        self.gridLayout_5.addWidget(self.Antibody_2, 8, 2, 1, 1)
        self.Smoking_2 = QtWidgets.QCheckBox(self.tab_4)
        self.Smoking_2.setChecked(True)
        self.Smoking_2.setObjectName("Smoking_2")
        self.gridLayout_5.addWidget(self.Smoking_2, 8, 1, 1, 1)
        self.Antibody_target_description_2 = QtWidgets.QCheckBox(self.tab_4)
        self.Antibody_target_description_2.setChecked(True)
        self.Antibody_target_description_2.setObjectName("Antibody_target_description_2")
        self.gridLayout_5.addWidget(self.Antibody_target_description_2, 13, 2, 2, 1)
        self.Phenotype_2 = QtWidgets.QCheckBox(self.tab_4)
        self.Phenotype_2.setChecked(True)
        self.Phenotype_2.setObjectName("Phenotype_2")
        self.gridLayout_5.addWidget(self.Phenotype_2, 14, 1, 1, 1)
        self.Cell_type_2 = QtWidgets.QCheckBox(self.tab_4)
        self.Cell_type_2.setChecked(True)
        self.Cell_type_2.setObjectName("Cell_type_2")
        self.gridLayout_5.addWidget(self.Cell_type_2, 13, 1, 1, 1)
        self.Cell_line_2 = QtWidgets.QCheckBox(self.tab_4)
        self.Cell_line_2.setChecked(True)
        self.Cell_line_2.setObjectName("Cell_line_2")
        self.gridLayout_5.addWidget(self.Cell_line_2, 12, 1, 1, 1)
        self.Genotype_2 = QtWidgets.QCheckBox(self.tab_4)
        self.Genotype_2.setChecked(True)
        self.Genotype_2.setObjectName("Genotype_2")
        self.gridLayout_5.addWidget(self.Genotype_2, 15, 1, 1, 1)
        self.Other_labels_2 = QtWidgets.QCheckBox(self.tab_4)
        self.Other_labels_2.setChecked(True)
        self.Other_labels_2.setObjectName("Other_labels_2")
        self.gridLayout_5.addWidget(self.Other_labels_2, 15, 2, 1, 1)
        self.Antibody_description_2 = QtWidgets.QCheckBox(self.tab_4)
        self.Antibody_description_2.setChecked(True)
        self.Antibody_description_2.setObjectName("Antibody_description_2")
        self.gridLayout_5.addWidget(self.Antibody_description_2, 11, 2, 2, 1)
        self.filter_and = QtWidgets.QPushButton(self.tab_4)
        self.filter_and.setObjectName("filter_and")
        self.gridLayout_5.addWidget(self.filter_and, 1, 0, 1, 1)
        self.filter_or = QtWidgets.QPushButton(self.tab_4)
        self.filter_or.setObjectName("filter_or")
        self.gridLayout_5.addWidget(self.filter_or, 1, 1, 1, 1)
        self.Survival_event_2 = QtWidgets.QCheckBox(self.tab_4)
        self.Survival_event_2.setChecked(True)
        self.Survival_event_2.setObjectName("Survival_event_2")
        self.gridLayout_5.addWidget(self.Survival_event_2, 8, 0, 1, 1)
        self.Survival_time_2 = QtWidgets.QCheckBox(self.tab_4)
        self.Survival_time_2.setChecked(True)
        self.Survival_time_2.setObjectName("Survival_time_2")
        self.gridLayout_5.addWidget(self.Survival_time_2, 9, 0, 1, 1)
        self.Primary_2 = QtWidgets.QCheckBox(self.tab_4)
        self.Primary_2.setChecked(True)
        self.Primary_2.setObjectName("Primary_2")
        self.gridLayout_5.addWidget(self.Primary_2, 10, 0, 1, 1)
        self.Metastasis_2 = QtWidgets.QCheckBox(self.tab_4)
        self.Metastasis_2.setChecked(True)
        self.Metastasis_2.setObjectName("Metastasis_2")
        self.gridLayout_5.addWidget(self.Metastasis_2, 11, 0, 1, 1)
        self.Therapy_2 = QtWidgets.QCheckBox(self.tab_4)
        self.Therapy_2.setChecked(True)
        self.Therapy_2.setObjectName("Therapy_2")
        self.gridLayout_5.addWidget(self.Therapy_2, 12, 0, 1, 1)
        self.Radiation_2 = QtWidgets.QCheckBox(self.tab_4)
        self.Radiation_2.setChecked(True)
        self.Radiation_2.setObjectName("Radiation_2")
        self.gridLayout_5.addWidget(self.Radiation_2, 13, 0, 1, 1)
        self.Response_2 = QtWidgets.QCheckBox(self.tab_4)
        self.Response_2.setChecked(True)
        self.Response_2.setObjectName("Response_2")
        self.gridLayout_5.addWidget(self.Response_2, 14, 0, 1, 1)
        self.tabWidget.addTab(self.tab_4, "")
        self.gridLayout_3.addWidget(self.tabWidget, 0, 6, 8, 1)
        self.progress_2 = QtWidgets.QLabel(self.groupBox_2)
        self.progress_2.setObjectName("progress_2")
        self.gridLayout_3.addWidget(self.progress_2, 5, 0, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem2, 5, 1, 1, 1)
        self.gridLayout_2.addWidget(self.groupBox_2, 2, 0, 1, 1)
        ArrayFetch.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(ArrayFetch)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1233, 26))
        self.menubar.setObjectName("menubar")
        self.menusettings = QtWidgets.QMenu(self.menubar)
        self.menusettings.setObjectName("menusettings")
        self.menuhelp = QtWidgets.QMenu(self.menubar)
        self.menuhelp.setObjectName("menuhelp")
        ArrayFetch.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(ArrayFetch)
        self.statusbar.setObjectName("statusbar")
        ArrayFetch.setStatusBar(self.statusbar)
        self.actionset_default_file_position = QtWidgets.QAction(ArrayFetch)
        self.actionset_default_file_position.setObjectName("actionset_default_file_position")
        self.actionhelp = QtWidgets.QAction(ArrayFetch)
        self.actionhelp.setObjectName("actionhelp")
        self.actionsave_parameters = QtWidgets.QAction(ArrayFetch)
        self.actionsave_parameters.setObjectName("actionsave_parameters")
        self.menusettings.addAction(self.actionset_default_file_position)
        self.menusettings.addAction(self.actionsave_parameters)
        self.menuhelp.addAction(self.actionhelp)
        self.menubar.addAction(self.menusettings.menuAction())
        self.menubar.addAction(self.menuhelp.menuAction())

        self.retranslateUi(ArrayFetch)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(ArrayFetch)

        self.set_file_position_btn.clicked.connect(self.choose_dir)
        self.set_file_position_btn.clicked.connect(self.set_dir)
        self.search_btn.clicked.connect(self.get_keyword)
        self.search_btn.clicked.connect(self.set_requires)
        self.search_btn.clicked.connect(self.start_fetch)
        self.download.clicked.connect(self.set_downloads)
        self.download.clicked.connect(self.start_download)
        self.open_file_btn.clicked.connect(self.choose_file)
        self.open_file_btn.clicked.connect(self.open_file)
        self.open_file_btn.clicked.connect(self.create_db)
        self.filter_and.clicked.connect(self.filter_1)
        self.filter_or.clicked.connect(self.filter_2)
        self.reverse_1.clicked.connect(self.toggle_1)
        self.reverse_2.clicked.connect(self.toggle_2)
        self.cancel_all_1.clicked.connect(self.cancel_all_10)
        self.select_all_1.clicked.connect(self.select_all_10)
        self.cancel_all_2.clicked.connect(self.cancel_all_20)
        self.select_all_2.clicked.connect(self.select_all_20)
        self.tableWidget.itemClicked.connect(self.outselect)
        self.tableWidget.itemDoubleClicked.connect(self.outselect2)
        self.excel.clicked.connect(self.export_to_excel)
        self.Cancer_type_1.stateChanged.connect(self.hidecolumn2)
        self.Tumor_location_1.stateChanged.connect(self.hidecolumn3)
        self.Tumor_grade_1.stateChanged.connect(self.hidecolumn4)
        self.Histology_1.stateChanged.connect(self.hidecolumn5)
        self.Stage_1.stateChanged.connect(self.hidecolumn6)
        self.Survival_event_1.stateChanged.connect(self.hidecolumn7)
        self.Survival_time_1.stateChanged.connect(self.hidecolumn8)
        self.Primary_1.stateChanged.connect(self.hidecolumn9)
        self.Metastasis_1.stateChanged.connect(self.hidecolumn10)
        self.Therapy_1.stateChanged.connect(self.hidecolumn11)
        self.Radiation_1.stateChanged.connect(self.hidecolumn12)
        self.Response_1.stateChanged.connect(self.hidecolumn13)
        self.Sample_info_1.stateChanged.connect(self.hidecolumn14)
        self.Organism_1.stateChanged.connect(self.hidecolumn15)
        self.Age_1.stateChanged.connect(self.hidecolumn16)
        self.Gender_1.stateChanged.connect(self.hidecolumn17)
        self.Ethnicity_1.stateChanged.connect(self.hidecolumn18)
        self.Smoking_1.stateChanged.connect(self.hidecolumn19)
        self.Pack_years_1.stateChanged.connect(self.hidecolumn20)
        self.Alcohol_1.stateChanged.connect(self.hidecolumn21)
        self.Tissue_1.stateChanged.connect(self.hidecolumn22)
        self.Cell_line_1.stateChanged.connect(self.hidecolumn23)
        self.Cell_type_1.stateChanged.connect(self.hidecolumn24)
        self.Phenotype_1.stateChanged.connect(self.hidecolumn25)
        self.Genotype_1.stateChanged.connect(self.hidecolumn26)
        self.Treatment_1.stateChanged.connect(self.hidecolumn27)
        self.shRNA_1.stateChanged.connect(self.hidecolumn28)
        self.RNAi_1.stateChanged.connect(self.hidecolumn29)
        self.Pulldown_1.stateChanged.connect(self.hidecolumn30)
        self.Transfection_1.stateChanged.connect(self.hidecolumn31)
        self.Antibody_1.stateChanged.connect(self.hidecolumn32)
        self.Antibody_vendor_1.stateChanged.connect(self.hidecolumn33)
        self.Antibody_description_1.stateChanged.connect(self.hidecolumn34)
        self.Antibody_target_description_1.stateChanged.connect(self.hidecolumn35)
        self.Other_labels_1.stateChanged.connect(self.hidecolumn36)
        self.Cancer_type_2.stateChanged.connect(self.gather1)
        self.Tumor_location_2.stateChanged.connect(self.gather2)
        self.Tumor_grade_2.stateChanged.connect(self.gather3)
        self.Histology_2.stateChanged.connect(self.gather4)
        self.Stage_2.stateChanged.connect(self.gather5)
        self.Survival_event_2.stateChanged.connect(self.gather6)
        self.Survival_time_2.stateChanged.connect(self.gather7)
        self.Primary_2.stateChanged.connect(self.gather8)
        self.Metastasis_2.stateChanged.connect(self.gather9)
        self.Therapy_2.stateChanged.connect(self.gather10)
        self.Radiation_2.stateChanged.connect(self.gather11)
        self.Response_2.stateChanged.connect(self.gather12)
        self.Sample_info_2.stateChanged.connect(self.gather13)
        self.Organism_2.stateChanged.connect(self.gather14)
        self.Age_2.stateChanged.connect(self.gather15)
        self.Gender_2.stateChanged.connect(self.gather16)
        self.Ethnicity_2.stateChanged.connect(self.gather17)
        self.Smoking_2.stateChanged.connect(self.gather18)
        self.Pack_years_2.stateChanged.connect(self.gather19)
        self.Alcohol_2.stateChanged.connect(self.gather20)
        self.Tissue_2.stateChanged.connect(self.gather21)
        self.Cell_line_2.stateChanged.connect(self.gather22)
        self.Cell_type_2.stateChanged.connect(self.gather23)
        self.Phenotype_2.stateChanged.connect(self.gather24)
        self.Genotype_2.stateChanged.connect(self.gather25)
        self.Treatment_2.stateChanged.connect(self.gather26)
        self.shRNA_2.stateChanged.connect(self.gather27)
        self.RNAi_2.stateChanged.connect(self.gather28)
        self.Pulldown_2.stateChanged.connect(self.gather29)
        self.Transfection_2.stateChanged.connect(self.gather30)
        self.Antibody_2.stateChanged.connect(self.gather31)
        self.Antibody_vendor_2.stateChanged.connect(self.gather32)
        self.Antibody_description_2.stateChanged.connect(self.gather33)
        self.Antibody_target_description_2.stateChanged.connect(self.gather34)
        self.Other_labels_2.stateChanged.connect(self.gather35)
        self.spinBox.valueChanged.connect(self.set_rest)
        self.actionset_default_file_position.triggered.connect(self.set_default)
        self.comboBox.currentTextChanged.connect(self.set_mode)
        self.actionsave_parameters.triggered.connect(self.save_parameter)
        global rest
        rest = self.spinBox.value()
        global mode
        mode = self.comboBox.currentText()

    def save_parameter(self):
        global parameters
        parameters = [self.Cancer_type_1.checkState(),
                      self.Tumor_location_1.checkState(),
                      self.Tumor_grade_1.checkState(),
                      self.Histology_1.checkState(),
                      self.Stage_1.checkState(),
                      self.Survival_event_1.checkState(),
                      self.Survival_time_1.checkState(),
                      self.Primary_1.checkState(),
                      self.Metastasis_1.checkState(),
                      self.Therapy_1.checkState(),
                      self.Radiation_1.checkState(),
                      self.Response_1.checkState(),
                      self.Sample_info_1.checkState(),
                      self.Organism_1.checkState(),
                      self.Age_1.checkState(),
                      self.Gender_1.checkState(),
                      self.Ethnicity_1.checkState(),
                      self.Smoking_1.checkState(),
                      self.Pack_years_1.checkState(),
                      self.Alcohol_1.checkState(),
                      self.Tissue_1.checkState(),
                      self.Cell_line_1.checkState(),
                      self.Cell_type_1.checkState(),
                      self.Phenotype_1.checkState(),
                      self.Genotype_1.checkState(),
                      self.Treatment_1.checkState(),
                      self.shRNA_1.checkState(),
                      self.RNAi_1.checkState(),
                      self.Pulldown_1.checkState(),
                      self.Transfection_1.checkState(),
                      self.Antibody_1.checkState(),
                      self.Antibody_vendor_1.checkState(),
                      self.Antibody_description_1.checkState(),
                      self.Antibody_target_description_1.checkState(),
                      self.Other_labels_1.checkState(),
                      self.Cancer_type_2.checkState(),
                      self.Tumor_location_2.checkState(),
                      self.Tumor_grade_2.checkState(),
                      self.Histology_2.checkState(),
                      self.Stage_2.checkState(),
                      self.Survival_event_2.checkState(),
                      self.Survival_time_2.checkState(),
                      self.Primary_2.checkState(),
                      self.Metastasis_2.checkState(),
                      self.Therapy_2.checkState(),
                      self.Radiation_2.checkState(),
                      self.Response_2.checkState(),
                      self.Sample_info_2.checkState(),
                      self.Organism_2.checkState(),
                      self.Age_2.checkState(),
                      self.Gender_2.checkState(),
                      self.Ethnicity_2.checkState(),
                      self.Smoking_2.checkState(),
                      self.Pack_years_2.checkState(),
                      self.Alcohol_2.checkState(),
                      self.Tissue_2.checkState(),
                      self.Cell_line_2.checkState(),
                      self.Cell_type_2.checkState(),
                      self.Phenotype_2.checkState(),
                      self.Genotype_2.checkState(),
                      self.Treatment_2.checkState(),
                      self.shRNA_2.checkState(),
                      self.RNAi_2.checkState(),
                      self.Pulldown_2.checkState(),
                      self.Transfection_2.checkState(),
                      self.Antibody_2.checkState(),
                      self.Antibody_vendor_2.checkState(),
                      self.Antibody_description_2.checkState(),
                      self.Antibody_target_description_2.checkState(),
                      self.Other_labels_2.checkState()]
        with open(os.getcwd() + "\\parameters\\parameters.txt", "w", encoding="utf-8") as f:
            for i in parameters:
                f.write(str(i) + "\n")

    def gather1(self, State):
        global gather_list
        if not State:
            gather_list.remove(1)
        else:
            gather_list.append(1)
            gather_list = sorted(gather_list)

    def gather2(self, State):
        global gather_list
        if not State:
            gather_list.remove(2)
        else:
            gather_list.append(2)
            gather_list = sorted(gather_list)

    def gather3(self, State):
        global gather_list
        if not State:
            gather_list.remove(3)
        else:
            gather_list.append(3)
            gather_list = sorted(gather_list)

    def gather4(self, State):
        global gather_list
        if not State:
            gather_list.remove(4)
        else:
            gather_list.append(4)
            gather_list = sorted(gather_list)

    def gather5(self, State):
        global gather_list
        if not State:
            gather_list.remove(5)
        else:
            gather_list.append(5)
            gather_list = sorted(gather_list)

    def gather6(self, State):
        global gather_list
        if not State:
            gather_list.remove(6)
        else:
            gather_list.append(6)
            gather_list = sorted(gather_list)

    def gather7(self, State):
        global gather_list
        if not State:
            gather_list.remove(7)
        else:
            gather_list.append(7)
            gather_list = sorted(gather_list)

    def gather8(self, State):
        global gather_list
        if not State:
            gather_list.remove(8)
        else:
            gather_list.append(8)
            gather_list = sorted(gather_list)

    def gather9(self, State):
        global gather_list
        if not State:
            gather_list.remove(9)
        else:
            gather_list.append(9)
            gather_list = sorted(gather_list)

    def gather10(self, State):
        global gather_list
        if not State:
            gather_list.remove(10)
        else:
            gather_list.append(10)
            gather_list = sorted(gather_list)

    def gather11(self, State):
        global gather_list
        if not State:
            gather_list.remove(11)
        else:
            gather_list.append(11)
            gather_list = sorted(gather_list)

    def gather12(self, State):
        global gather_list
        if not State:
            gather_list.remove(12)
        else:
            gather_list.append(12)
            gather_list = sorted(gather_list)

    def gather13(self, State):
        global gather_list
        if not State:
            gather_list.remove(13)
        else:
            gather_list.append(13)
            gather_list = sorted(gather_list)

    def gather14(self, State):
        global gather_list
        if not State:
            gather_list.remove(14)
        else:
            gather_list.append(14)
            gather_list = sorted(gather_list)

    def gather15(self, State):
        global gather_list
        if not State:
            gather_list.remove(15)
        else:
            gather_list.append(15)
            gather_list = sorted(gather_list)

    def gather16(self, State):
        global gather_list
        if not State:
            gather_list.remove(16)
        else:
            gather_list.append(16)
            gather_list = sorted(gather_list)

    def gather17(self, State):
        global gather_list
        if not State:
            gather_list.remove(17)
        else:
            gather_list.append(17)
            gather_list = sorted(gather_list)

    def gather18(self, State):
        global gather_list
        if not State:
            gather_list.remove(18)
        else:
            gather_list.append(18)
            gather_list = sorted(gather_list)

    def gather19(self, State):
        global gather_list
        if not State:
            gather_list.remove(19)
        else:
            gather_list.append(19)
            gather_list = sorted(gather_list)

    def gather20(self, State):
        global gather_list
        if not State:
            gather_list.remove(20)
        else:
            gather_list.append(20)
            gather_list = sorted(gather_list)

    def gather21(self, State):
        global gather_list
        if not State:
            gather_list.remove(21)
        else:
            gather_list.append(21)
            gather_list = sorted(gather_list)

    def gather22(self, State):
        global gather_list
        if not State:
            gather_list.remove(22)
        else:
            gather_list.append(22)
            gather_list = sorted(gather_list)

    def gather23(self, State):
        global gather_list
        if not State:
            gather_list.remove(23)
        else:
            gather_list.append(23)
            gather_list = sorted(gather_list)

    def gather24(self, State):
        global gather_list
        if not State:
            gather_list.remove(24)
        else:
            gather_list.append(24)
            gather_list = sorted(gather_list)

    def gather25(self, State):
        global gather_list
        if not State:
            gather_list.remove(25)
        else:
            gather_list.append(25)
            gather_list = sorted(gather_list)

    def gather26(self, State):
        global gather_list
        if not State:
            gather_list.remove(26)
        else:
            gather_list.append(26)
            gather_list = sorted(gather_list)

    def gather27(self, State):
        global gather_list
        if not State:
            gather_list.remove(27)
        else:
            gather_list.append(27)
            gather_list = sorted(gather_list)

    def gather28(self, State):
        global gather_list
        if not State:
            gather_list.remove(28)
        else:
            gather_list.append(28)
            gather_list = sorted(gather_list)

    def gather29(self, State):
        global gather_list
        if not State:
            gather_list.remove(29)
        else:
            gather_list.append(29)
            gather_list = sorted(gather_list)

    def gather30(self, State):
        global gather_list
        if not State:
            gather_list.remove(30)
        else:
            gather_list.append(30)
            gather_list = sorted(gather_list)

    def gather31(self, State):
        global gather_list
        if not State:
            gather_list.remove(31)
        else:
            gather_list.append(31)
            gather_list = sorted(gather_list)

    def gather32(self, State):
        global gather_list
        if not State:
            gather_list.remove(32)
        else:
            gather_list.append(32)
            gather_list = sorted(gather_list)

    def gather33(self, State):
        global gather_list
        if not State:
            gather_list.remove(33)
        else:
            gather_list.append(33)
            gather_list = sorted(gather_list)

    def gather34(self, State):
        global gather_list
        if not State:
            gather_list.remove(34)
        else:
            gather_list.append(34)
            gather_list = sorted(gather_list)

    def gather35(self, State):
        global gather_list
        if not State:
            gather_list.remove(35)
        else:
            gather_list.append(35)
            gather_list = sorted(gather_list)

    def set_mode(self):
        global mode
        mode = self.comboBox.currentText()

    def set_default(self):
        global file_position
        file_position = QFileDialog.getExistingDirectory(self, "choose a directory")
        with open(os.getcwd() + "\\default file position\\default.txt", "w", encoding="utf-8") as f:
            f.write(file_position)
        self.file_position.setText(file_position)

    def set_rest(self):
        global rest
        rest = self.spinBox.value()

    def start_fetch(self):
            self.thread = fetch_thread.Job(rest, mode)
            self.thread.signal.connect(self.use_progress)
            self.thread.start()

    def start_download(self):
        if download_set:
            self.thread = download_files.Job(rest)
            self.thread.signal.connect(self.use_progress2)
            self.thread.start()

    def create_db(self):
        if file_name:
            conn = sqlite3.connect(file_name.strip(".txt") + ".db")
            c = conn.cursor()
            try:
                c.execute("DROP TABLE SHEET")
            except:
                pass
            c.execute('''CREATE TABLE SHEET
                            (ID INT PRIMARY KEY,
                            accesion_number TEXT,
                            experiment_type TEXT,
                            release_date TEXT,
                            title TEXT,
                            description TEXT,
                            array TEXT,
                            protocol_name TEXT,
                            protocol_description TEXT,
                            protocol_hardware TEXT,
                            pubmed_id TEXT,
                            platform TEXT,
                            cancer_type TEXT,
                            tumor_location TEXT,
                            tumor_grade TEXT,
                            histology TEXT,
                            stage TEXT,
                            survival_event TEXT,
                            survival_time TEXT,
                            pri_mary TEXT,
                            metastasis TEXT,
                            therapy TEXT,
                            radiation TEXT,
                            response TEXT,
                            sample_info TEXT,
                            organism TEXT,
                            age TEXT,
                            gender TEXT,
                            ethnicity TEXT,
                            smoking TEXT,
                            pack_years TEXT,
                            alcohol TEXT,
                            tissue TEXT,
                            cell_line TEXT,
                            cell_type TEXT,
                            phenotype TEXT,
                            genotype TEXT,
                            treatment TEXT,
                            shrna TEXT,
                            rnai TEXT,
                            pulldown TEXT,
                            transfection TEXT,
                            antibody TEXT,
                            antibody_vendor TEXT,
                            antibody_description TEXT,
                            antibody_target_description TEXT,
                            other_labels TEXT);''')
            with open(file_name, encoding="utf-8")as f:
                id = 0
                while True:
                    id += 1
                    line = f.readline()
                    if line:
                        line = line.split('\t')
                        count = -1
                        for i in line:
                            count += 1
                            line[count] = i.strip().replace("\'", "\'\'")
                        temp = "(" + str(id) + ", "
                        for i in line:
                            if i == "":
                                temp = temp + "NULL, "
                            else:
                                temp = temp + "\'" + i + "\', "
                        temp = temp.strip(", ") + ")"
                        c.execute("INSERT INTO SHEET (ID,accesion_number,experiment_type,release_date,title,description,\
                                          array,protocol_name,protocol_description,protocol_hardware,pubmed_id,platform,"
                                  "cancer_type,tumor_location,tumor_grade,histology,stage,survival_event,survival_time,"
                                  "pri_mary,metastasis,therapy,radiation,response,sample_info,organism,age,gender,"
                                  "ethnicity,smoking,pack_years,alcohol,tissue,cell_line,cell_type,"
                                  "phenotype,genotype,treatment,shrna,rnai,pulldown,transfection,antibody,"
                                  "antibody_vendor,antibody_description,antibody_target_description,other_labels) \
                                  VALUES " + temp)
                    else:
                        break
                conn.commit()
                conn.close()
        else:
            pass

    def filter_1(self):
        if file_name:
            if gather_list:
                gather_list2 = []
                conn = sqlite3.connect(file_name.strip(".txt") + ".db")
                c = conn.cursor()
                try:
                    gather_list.remove(0)
                except:
                    pass
                for i in gather_list:
                    gather_list2.append(db_library[i])
                temp = ""
                for i in gather_list2:
                    temp = temp + i + " IS NOT NULL AND "
                temp = temp.strip(" AND ")
                cursor = c.execute("SELECT * " + " from SHEET WHERE " + temp)
                self.tableWidget.setRowCount(0)
                for row in cursor:
                    if row:
                        row = row[1:]
                        row_count = self.tableWidget.rowCount()
                        self.tableWidget.insertRow(row_count)
                        count = -1
                        for i in row:
                            count = count + 1
                            self.tableWidget.setItem(row_count, count, QtWidgets.QTableWidgetItem(i))
                    else:
                        break
                conn.close()
            else:
                pass
        else:
            pass

    def filter_2(self):
        if file_name:
            if gather_list:
                gather_list2 = []
                conn = sqlite3.connect(file_name.strip(".txt") + ".db")
                c = conn.cursor()
                try:
                    gather_list.remove(0)
                except:
                    pass
                for i in gather_list:
                    gather_list2.append(db_library[i])
                temp = ""
                for i in gather_list2:
                    temp = temp + i + " IS NOT NULL OR "
                temp = temp.strip(" OR ")
                cursor = c.execute("SELECT * " + " from SHEET WHERE " + temp)
                self.tableWidget.setRowCount(0)
                for row in cursor:
                    if row:
                        row = row[1:]
                        row_count = self.tableWidget.rowCount()
                        self.tableWidget.insertRow(row_count)
                        count = -1
                        for i in row:
                            count = count + 1
                            self.tableWidget.setItem(row_count, count, QtWidgets.QTableWidgetItem(i))
                    else:
                        break
                conn.close()
            else:
                pass
        else:
            pass

    def toggle_1(self):
        self.Cancer_type_1.toggle()
        self.Tumor_location_1.toggle()
        self.Tumor_grade_1.toggle()
        self.Histology_1.toggle()
        self.Stage_1.toggle()
        self.Survival_event_1.toggle()
        self.Survival_time_1.toggle()
        self.Primary_1.toggle()
        self.Metastasis_1.toggle()
        self.Therapy_1.toggle()
        self.Radiation_1.toggle()
        self.Response_1.toggle()
        self.Sample_info_1.toggle()
        self.Organism_1.toggle()
        self.Age_1.toggle()
        self.Gender_1.toggle()
        self.Ethnicity_1.toggle()
        self.Smoking_1.toggle()
        self.Pack_years_1.toggle()
        self.Alcohol_1.toggle()
        self.Tissue_1.toggle()
        self.Cell_line_1.toggle()
        self.Cell_type_1.toggle()
        self.Phenotype_1.toggle()
        self.Genotype_1.toggle()
        self.Treatment_1.toggle()
        self.shRNA_1.toggle()
        self.RNAi_1.toggle()
        self.Pulldown_1.toggle()
        self.Transfection_1.toggle()
        self.Antibody_1.toggle()
        self.Antibody_vendor_1.toggle()
        self.Antibody_description_1.toggle()
        self.Antibody_target_description_1.toggle()
        self.Other_labels_1.toggle()

    def toggle_2(self):
        self.Cancer_type_2.toggle()
        self.Tumor_location_2.toggle()
        self.Tumor_grade_2.toggle()
        self.Histology_2.toggle()
        self.Stage_2.toggle()
        self.Survival_event_2.toggle()
        self.Survival_time_2.toggle()
        self.Primary_2.toggle()
        self.Metastasis_2.toggle()
        self.Therapy_2.toggle()
        self.Radiation_2.toggle()
        self.Response_2.toggle()
        self.Sample_info_2.toggle()
        self.Organism_2.toggle()
        self.Age_2.toggle()
        self.Gender_2.toggle()
        self.Ethnicity_2.toggle()
        self.Smoking_2.toggle()
        self.Pack_years_2.toggle()
        self.Alcohol_2.toggle()
        self.Tissue_2.toggle()
        self.Cell_line_2.toggle()
        self.Cell_type_2.toggle()
        self.Phenotype_2.toggle()
        self.Genotype_2.toggle()
        self.Treatment_2.toggle()
        self.shRNA_2.toggle()
        self.RNAi_2.toggle()
        self.Pulldown_2.toggle()
        self.Transfection_2.toggle()
        self.Antibody_2.toggle()
        self.Antibody_vendor_2.toggle()
        self.Antibody_description_2.toggle()
        self.Antibody_target_description_2.toggle()
        self.Other_labels_2.toggle()

    def use_progress(self, msg1, msg2):
        self.progress.setText(msg1)
        self.progressBar.setValue(msg2)

    def use_progress2(self, msg1, msg2):
        self.progress_2.setText(msg1)
        self.progressBar_2.setValue(msg2)

    def outselect(self, Item):
        self.plainTextEdit.setPlainText(Item.text())

    def outselect2(self, Item):
        global download_set
        i = self.tableWidget.item(Item.row(), 0).text()
        if i not in download_set:
            download_set.add(i)
        else:
            download_set.remove(i)
        download_list = ""
        for i in download_set:
            download_list = download_list + i + "\n"
        self.plainTextEdit_2.clear()
        self.plainTextEdit_2.setPlainText(download_list)

    def cancel_all_10(self):
        self.Cancer_type_1.setChecked(0)
        self.Tumor_location_1.setChecked(0)
        self.Tumor_grade_1.setChecked(0)
        self.Histology_1.setChecked(0)
        self.Stage_1.setChecked(0)
        self.Survival_event_1.setChecked(0)
        self.Survival_time_1.setChecked(0)
        self.Primary_1.setChecked(0)
        self.Metastasis_1.setChecked(0)
        self.Therapy_1.setChecked(0)
        self.Radiation_1.setChecked(0)
        self.Response_1.setChecked(0)
        self.Sample_info_1.setChecked(0)
        self.Organism_1.setChecked(0)
        self.Age_1.setChecked(0)
        self.Gender_1.setChecked(0)
        self.Ethnicity_1.setChecked(0)
        self.Smoking_1.setChecked(0)
        self.Pack_years_1.setChecked(0)
        self.Alcohol_1.setChecked(0)
        self.Tissue_1.setChecked(0)
        self.Cell_line_1.setChecked(0)
        self.Cell_type_1.setChecked(0)
        self.Phenotype_1.setChecked(0)
        self.Genotype_1.setChecked(0)
        self.Treatment_1.setChecked(0)
        self.shRNA_1.setChecked(0)
        self.RNAi_1.setChecked(0)
        self.Pulldown_1.setChecked(0)
        self.Transfection_1.setChecked(0)
        self.Antibody_1.setChecked(0)
        self.Antibody_vendor_1.setChecked(0)
        self.Antibody_description_1.setChecked(0)
        self.Antibody_target_description_1.setChecked(0)
        self.Other_labels_1.setChecked(0)

    def select_all_10(self):
        self.Cancer_type_1.setChecked(1)
        self.Tumor_location_1.setChecked(1)
        self.Tumor_grade_1.setChecked(1)
        self.Histology_1.setChecked(1)
        self.Stage_1.setChecked(1)
        self.Survival_event_1.setChecked(1)
        self.Survival_time_1.setChecked(1)
        self.Primary_1.setChecked(1)
        self.Metastasis_1.setChecked(1)
        self.Therapy_1.setChecked(1)
        self.Radiation_1.setChecked(1)
        self.Response_1.setChecked(1)
        self.Sample_info_1.setChecked(1)
        self.Organism_1.setChecked(1)
        self.Age_1.setChecked(1)
        self.Gender_1.setChecked(1)
        self.Ethnicity_1.setChecked(1)
        self.Smoking_1.setChecked(1)
        self.Pack_years_1.setChecked(1)
        self.Alcohol_1.setChecked(1)
        self.Tissue_1.setChecked(1)
        self.Cell_line_1.setChecked(1)
        self.Cell_type_1.setChecked(1)
        self.Phenotype_1.setChecked(1)
        self.Genotype_1.setChecked(1)
        self.Treatment_1.setChecked(1)
        self.shRNA_1.setChecked(1)
        self.RNAi_1.setChecked(1)
        self.Pulldown_1.setChecked(1)
        self.Transfection_1.setChecked(1)
        self.Antibody_1.setChecked(1)
        self.Antibody_vendor_1.setChecked(1)
        self.Antibody_description_1.setChecked(1)
        self.Antibody_target_description_1.setChecked(1)
        self.Other_labels_1.setChecked(1)

    def cancel_all_20(self):
        self.Cancer_type_2.setChecked(0)
        self.Tumor_location_2.setChecked(0)
        self.Tumor_grade_2.setChecked(0)
        self.Histology_2.setChecked(0)
        self.Stage_2.setChecked(0)
        self.Survival_event_2.setChecked(0)
        self.Survival_time_2.setChecked(0)
        self.Primary_2.setChecked(0)
        self.Metastasis_2.setChecked(0)
        self.Therapy_2.setChecked(0)
        self.Radiation_2.setChecked(0)
        self.Response_2.setChecked(0)
        self.Sample_info_2.setChecked(0)
        self.Organism_2.setChecked(0)
        self.Age_2.setChecked(0)
        self.Gender_2.setChecked(0)
        self.Ethnicity_2.setChecked(0)
        self.Smoking_2.setChecked(0)
        self.Pack_years_2.setChecked(0)
        self.Alcohol_2.setChecked(0)
        self.Tissue_2.setChecked(0)
        self.Cell_line_2.setChecked(0)
        self.Cell_type_2.setChecked(0)
        self.Phenotype_2.setChecked(0)
        self.Genotype_2.setChecked(0)
        self.Treatment_2.setChecked(0)
        self.shRNA_2.setChecked(0)
        self.RNAi_2.setChecked(0)
        self.Pulldown_2.setChecked(0)
        self.Transfection_2.setChecked(0)
        self.Antibody_2.setChecked(0)
        self.Antibody_vendor_2.setChecked(0)
        self.Antibody_description_2.setChecked(0)
        self.Antibody_target_description_2.setChecked(0)
        self.Other_labels_2.setChecked(0)

    def select_all_20(self):
        self.Cancer_type_2.setChecked(1)
        self.Tumor_location_2.setChecked(1)
        self.Tumor_grade_2.setChecked(1)
        self.Histology_2.setChecked(1)
        self.Stage_2.setChecked(1)
        self.Survival_event_2.setChecked(1)
        self.Survival_time_2.setChecked(1)
        self.Primary_2.setChecked(1)
        self.Metastasis_2.setChecked(1)
        self.Therapy_2.setChecked(1)
        self.Radiation_2.setChecked(1)
        self.Response_2.setChecked(1)
        self.Sample_info_2.setChecked(1)
        self.Organism_2.setChecked(1)
        self.Age_2.setChecked(1)
        self.Gender_2.setChecked(1)
        self.Ethnicity_2.setChecked(1)
        self.Smoking_2.setChecked(1)
        self.Pack_years_2.setChecked(1)
        self.Alcohol_2.setChecked(1)
        self.Tissue_2.setChecked(1)
        self.Cell_line_2.setChecked(1)
        self.Cell_type_2.setChecked(1)
        self.Phenotype_2.setChecked(1)
        self.Genotype_2.setChecked(1)
        self.Treatment_2.setChecked(1)
        self.shRNA_2.setChecked(1)
        self.RNAi_2.setChecked(1)
        self.Pulldown_2.setChecked(1)
        self.Transfection_2.setChecked(1)
        self.Antibody_2.setChecked(1)
        self.Antibody_vendor_2.setChecked(1)
        self.Antibody_description_2.setChecked(1)
        self.Antibody_target_description_2.setChecked(1)
        self.Other_labels_2.setChecked(1)

    def export_to_excel(self):

        file_existence = 1
        try:
            f = open(file_name.strip(".txt") + ".xls")
            f.close()
        except IOError:
            file_existence = 0

        if file_existence == 0:
            f = open(file_name, encoding="utf-8")
            x = 0
            y = 0
            xls = xlwt.Workbook()
            sheet = xls.add_sheet('sheet1', cell_overwrite_ok=True)
            while True:
                line = f.readline()
                if not line:
                    break
                for i in line.split("\t"):
                    sheet.write(x, y, i)
                    y += 1
                x += 1
                y = 0
            f.close()
            xls.save(file_name.strip(".txt") + '.xls')
        else:
            os.remove(file_name.strip(".txt") + ".xls")
            f = open(file_name, encoding="utf-8")
            x = 0
            y = 0
            xls = xlwt.Workbook()
            sheet = xls.add_sheet('sheet1', cell_overwrite_ok=True)
            while True:
                line = f.readline()
                if not line:
                    break
                for i in line.split("\t"):
                    sheet.write(x, y, i)
                    y += 1
                x += 1
                y = 0
            f.close()
            xls.save(file_name.strip(".txt") + '.xls')

    def hidecolumn2(self, State):
        if State:
            self.tableWidget.showColumn(11)
        else:
            self.tableWidget.hideColumn(11)

    def hidecolumn3(self, State):
        if State:
            self.tableWidget.showColumn(12)
        else:
            self.tableWidget.hideColumn(12)

    def hidecolumn4(self, State):
        if State:
            self.tableWidget.showColumn(13)
        else:
            self.tableWidget.hideColumn(13)

    def hidecolumn5(self, State):
        if State:
            self.tableWidget.showColumn(14)
        else:
            self.tableWidget.hideColumn(14)

    def hidecolumn6(self, State):
        if State:
            self.tableWidget.showColumn(15)
        else:
            self.tableWidget.hideColumn(15)

    def hidecolumn7(self, State):
        if State:
            self.tableWidget.showColumn(16)
        else:
            self.tableWidget.hideColumn(16)

    def hidecolumn8(self, State):
        if State:
            self.tableWidget.showColumn(17)
        else:
            self.tableWidget.hideColumn(17)

    def hidecolumn9(self, State):
        if State:
            self.tableWidget.showColumn(18)
        else:
            self.tableWidget.hideColumn(18)

    def hidecolumn10(self, State):
        if State:
            self.tableWidget.showColumn(19)
        else:
            self.tableWidget.hideColumn(19)

    def hidecolumn11(self, State):
        if State:
            self.tableWidget.showColumn(20)
        else:
            self.tableWidget.hideColumn(20)

    def hidecolumn12(self, State):
        if State:
            self.tableWidget.showColumn(21)
        else:
            self.tableWidget.hideColumn(21)

    def hidecolumn13(self, State):
        if State:
            self.tableWidget.showColumn(22)
        else:
            self.tableWidget.hideColumn(22)

    def hidecolumn14(self, State):
        if State:
            self.tableWidget.showColumn(23)
        else:
            self.tableWidget.hideColumn(23)

    def hidecolumn15(self, State):
        if State:
            self.tableWidget.showColumn(24)
        else:
            self.tableWidget.hideColumn(24)

    def hidecolumn16(self, State):
        if State:
            self.tableWidget.showColumn(25)
        else:
            self.tableWidget.hideColumn(25)

    def hidecolumn17(self, State):
        if State:
            self.tableWidget.showColumn(26)
        else:
            self.tableWidget.hideColumn(26)

    def hidecolumn18(self, State):
        if State:
            self.tableWidget.showColumn(27)
        else:
            self.tableWidget.hideColumn(27)

    def hidecolumn19(self, State):
        if State:
            self.tableWidget.showColumn(28)
        else:
            self.tableWidget.hideColumn(28)

    def hidecolumn20(self, State):
        if State:
            self.tableWidget.showColumn(29)
        else:
            self.tableWidget.hideColumn(29)

    def hidecolumn21(self, State):
        if State:
            self.tableWidget.showColumn(30)
        else:
            self.tableWidget.hideColumn(30)

    def hidecolumn22(self, State):
        if State:
            self.tableWidget.showColumn(31)
        else:
            self.tableWidget.hideColumn(31)

    def hidecolumn23(self, State):
        if State:
            self.tableWidget.showColumn(32)
        else:
            self.tableWidget.hideColumn(32)

    def hidecolumn24(self, State):
        if State:
            self.tableWidget.showColumn(33)
        else:
            self.tableWidget.hideColumn(33)

    def hidecolumn25(self, State):
        if State:
            self.tableWidget.showColumn(34)
        else:
            self.tableWidget.hideColumn(34)

    def hidecolumn26(self, State):
        if State:
            self.tableWidget.showColumn(35)
        else:
            self.tableWidget.hideColumn(35)

    def hidecolumn27(self, State):
        if State:
            self.tableWidget.showColumn(36)
        else:
            self.tableWidget.hideColumn(36)

    def hidecolumn28(self, State):
        if State:
            self.tableWidget.showColumn(37)
        else:
            self.tableWidget.hideColumn(37)

    def hidecolumn29(self, State):
        if State:
            self.tableWidget.showColumn(38)
        else:
            self.tableWidget.hideColumn(38)

    def hidecolumn30(self, State):
        if State:
            self.tableWidget.showColumn(39)
        else:
            self.tableWidget.hideColumn(39)

    def hidecolumn31(self, State):
        if State:
            self.tableWidget.showColumn(40)
        else:
            self.tableWidget.hideColumn(40)

    def hidecolumn32(self, State):
        if State:
            self.tableWidget.showColumn(41)
        else:
            self.tableWidget.hideColumn(41)

    def hidecolumn33(self, State):
        if State:
            self.tableWidget.showColumn(42)
        else:
            self.tableWidget.hideColumn(42)

    def hidecolumn34(self, State):
        if State:
            self.tableWidget.showColumn(43)
        else:
            self.tableWidget.hideColumn(43)

    def hidecolumn35(self, State):
        if State:
            self.tableWidget.showColumn(44)
        else:
            self.tableWidget.hideColumn(44)

    def hidecolumn36(self, State):
        if State:
            self.tableWidget.showColumn(45)
        else:
            self.tableWidget.hideColumn(45)

    def retranslateUi(self, ArrayFetch):
        _translate = QtCore.QCoreApplication.translate
        ArrayFetch.setWindowTitle(_translate("ArrayFetch", "ArrayFetch"))
        ArrayFetch.setAccessibleName(_translate("ArrayFetch", "ArrayFetch"))
        self.groupBox.setToolTip(_translate("ArrayFetch", "press search to collect and download data from ArrayExpress"))
        self.groupBox.setTitle(_translate("ArrayFetch", "search && fetch"))
        self.file_position.setPlaceholderText(_translate("ArrayFetch", "please select or input an existing directory"))
        self.input_keywords.setPlaceholderText(_translate("ArrayFetch", "please check the rule of ArrayExpress searching"))
        self.progress.setText(_translate("ArrayFetch", "status: Unstarted"))
        self.search_btn.setText(_translate("ArrayFetch", "search"))
        self.label.setText(_translate("ArrayFetch", "rest time"))
        self.label_2.setText(_translate("ArrayFetch", "mode"))
        self.set_file_position_btn.setText(_translate("ArrayFetch", "file position..."))
        self.comboBox.setItemText(0, _translate("ArrayFetch", "Normal"))
        self.comboBox.setItemText(1, _translate("ArrayFetch", "Cell line focus"))
        self.comboBox.setItemText(2, _translate("ArrayFetch", "Not sorted"))
        self.comboBox.setItemText(3, _translate("ArrayFetch", "Raw"))
        self.excel.setText(_translate("ArrayFetch", "export to excel file"))
        self.plainTextEdit.setPlaceholderText(_translate("ArrayFetch", "click a table cell to show detailed information"))
        self.open_file_btn.setText(_translate("ArrayFetch", "open file"))
        self.download.setText(_translate("ArrayFetch", "download"))
        self.Age_1.setText(_translate("ArrayFetch", "Age"))
        self.Histology_1.setText(_translate("ArrayFetch", "Histology"))
        self.Cancer_type_1.setText(_translate("ArrayFetch", "Cancer type"))
        self.shRNA_1.setText(_translate("ArrayFetch", "shRNA"))
        self.Gender_1.setText(_translate("ArrayFetch", "Gender"))
        self.RNAi_1.setText(_translate("ArrayFetch", "RNAi"))
        self.Tumor_grade_1.setText(_translate("ArrayFetch", "Tumor grade"))
        self.Pulldown_1.setText(_translate("ArrayFetch", "Pulldown"))
        self.reverse_1.setText(_translate("ArrayFetch", "reverse"))
        self.Treatment_1.setText(_translate("ArrayFetch", "Treatment"))
        self.Stage_1.setText(_translate("ArrayFetch", "Stage"))
        self.Tumor_location_1.setText(_translate("ArrayFetch", "Tumor location"))
        self.Ethnicity_1.setText(_translate("ArrayFetch", "Ethnicity"))
        self.Transfection_1.setText(_translate("ArrayFetch", "Transfection"))
        self.cancel_all_1.setText(_translate("ArrayFetch", "cancel all"))
        self.Sample_info_1.setText(_translate("ArrayFetch", "Sample info"))
        self.Organism_1.setText(_translate("ArrayFetch", "Organism"))
        self.select_all_1.setText(_translate("ArrayFetch", "select all"))
        self.Alcohol_1.setText(_translate("ArrayFetch", "Alcohol"))
        self.Smoking_1.setText(_translate("ArrayFetch", "Smoking"))
        self.Antibody_vendor_1.setText(_translate("ArrayFetch", "Antibody\n"
"vendor"))
        self.Tissue_1.setText(_translate("ArrayFetch", "Tissue"))
        self.Antibody_description_1.setText(_translate("ArrayFetch", "Antibody\n"
"description"))
        self.Cell_line_1.setText(_translate("ArrayFetch", "Cell line"))
        self.Antibody_1.setText(_translate("ArrayFetch", "Antibody"))
        self.Pack_years_1.setText(_translate("ArrayFetch", "Pack years"))
        self.Phenotype_1.setText(_translate("ArrayFetch", "Phenotype"))
        self.Antibody_target_description_1.setText(_translate("ArrayFetch", "Antibody target\n"
"description"))
        self.Cell_type_1.setText(_translate("ArrayFetch", "Cell type"))
        self.label_4.setText(_translate("ArrayFetch", "-sample related-"))
        self.label_5.setText(_translate("ArrayFetch", "-treatment related-"))
        self.label_3.setText(_translate("ArrayFetch", "-cancer related-"))
        self.Genotype_1.setText(_translate("ArrayFetch", "Genotype"))
        self.Other_labels_1.setText(_translate("ArrayFetch", "Other labels"))
        self.Survival_event_1.setText(_translate("ArrayFetch", "Survival event"))
        self.Survival_time_1.setText(_translate("ArrayFetch", "Survival time"))
        self.Primary_1.setText(_translate("ArrayFetch", "Primary"))
        self.Metastasis_1.setText(_translate("ArrayFetch", "Metastasis"))
        self.Therapy_1.setText(_translate("ArrayFetch", "Therapy"))
        self.Radiation_1.setText(_translate("ArrayFetch", "Radiation"))
        self.Response_1.setText(_translate("ArrayFetch", "Response"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("ArrayFetch", "show/hide"))
        self.select_all_2.setText(_translate("ArrayFetch", "select all"))
        self.label_7.setText(_translate("ArrayFetch", "-sample related-"))
        self.label_9.setText(_translate("ArrayFetch", "-treatment related-"))
        self.Treatment_2.setText(_translate("ArrayFetch", "Treatment"))
        self.reverse_2.setText(_translate("ArrayFetch", "reverse"))
        self.Tumor_location_2.setText(_translate("ArrayFetch", "Tumor location"))
        self.cancel_all_2.setText(_translate("ArrayFetch", "cancel all"))
        self.label_6.setText(_translate("ArrayFetch", "-cancer related-"))
        self.Sample_info_2.setText(_translate("ArrayFetch", "Sample info"))
        self.Organism_2.setText(_translate("ArrayFetch", "Organism"))
        self.Cancer_type_2.setText(_translate("ArrayFetch", "Cancer type"))
        self.Pulldown_2.setText(_translate("ArrayFetch", "Pulldown"))
        self.Stage_2.setText(_translate("ArrayFetch", "Stage"))
        self.Tumor_grade_2.setText(_translate("ArrayFetch", "Tumor grade"))
        self.Gender_2.setText(_translate("ArrayFetch", "Gender"))
        self.shRNA_2.setText(_translate("ArrayFetch", "shRNA"))
        self.RNAi_2.setText(_translate("ArrayFetch", "RNAi"))
        self.Age_2.setText(_translate("ArrayFetch", "Age"))
        self.Histology_2.setText(_translate("ArrayFetch", "Histology"))
        self.Ethnicity_2.setText(_translate("ArrayFetch", "Ethnicity"))
        self.Transfection_2.setText(_translate("ArrayFetch", "Transfection"))
        self.Pack_years_2.setText(_translate("ArrayFetch", "Pack years"))
        self.Antibody_vendor_2.setText(_translate("ArrayFetch", "Antibody\n"
"vendor"))
        self.Tissue_2.setText(_translate("ArrayFetch", "Tissue"))
        self.Alcohol_2.setText(_translate("ArrayFetch", "Alcohol"))
        self.Antibody_2.setText(_translate("ArrayFetch", "Antibody"))
        self.Smoking_2.setText(_translate("ArrayFetch", "Smoking"))
        self.Antibody_target_description_2.setText(_translate("ArrayFetch", "Antibody target\n"
"description"))
        self.Phenotype_2.setText(_translate("ArrayFetch", "Phenotype"))
        self.Cell_type_2.setText(_translate("ArrayFetch", "Cell type"))
        self.Cell_line_2.setText(_translate("ArrayFetch", "Cell line"))
        self.Genotype_2.setText(_translate("ArrayFetch", "Genotype"))
        self.Other_labels_2.setText(_translate("ArrayFetch", "Other labels"))
        self.Antibody_description_2.setText(_translate("ArrayFetch", "Antibody\n"
"description"))
        self.filter_and.setText(_translate("ArrayFetch", "filter: and"))
        self.filter_or.setText(_translate("ArrayFetch", "fileter: or"))
        self.Survival_event_2.setText(_translate("ArrayFetch", "Survival event"))
        self.Survival_time_2.setText(_translate("ArrayFetch", "Survival time"))
        self.Primary_2.setText(_translate("ArrayFetch", "Primary"))
        self.Metastasis_2.setText(_translate("ArrayFetch", "Metastasis"))
        self.Therapy_2.setText(_translate("ArrayFetch", "Therapy"))
        self.Radiation_2.setText(_translate("ArrayFetch", "Radiation"))
        self.Response_2.setText(_translate("ArrayFetch", "Response"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4), _translate("ArrayFetch", "filter"))
        self.progress_2.setText(_translate("ArrayFetch", "status: Unstarted"))
        self.menusettings.setTitle(_translate("ArrayFetch", "settings"))
        self.menuhelp.setTitle(_translate("ArrayFetch", "help"))
        self.actionset_default_file_position.setText(_translate("ArrayFetch", "set default file position"))
        self.actionhelp.setText(_translate("ArrayFetch", "help"))
        self.actionsave_parameters.setText(_translate("ArrayFetch", "save parameters"))


class Ui_read_me(object):
    def setupUi(self, read_me):
        read_me.setObjectName("read_me")
        read_me.resize(651, 613)
        read_me.setMinimumSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        read_me.setFont(font)
        read_me.setSizeGripEnabled(True)
        self.gridLayout = QtWidgets.QGridLayout(read_me)
        self.gridLayout.setObjectName("gridLayout")
        self.plainTextEdit = QtWidgets.QPlainTextEdit(read_me)
        self.plainTextEdit.setReadOnly(True)
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.gridLayout.addWidget(self.plainTextEdit, 0, 0, 1, 1)

        self.retranslateUi(read_me)
        QtCore.QMetaObject.connectSlotsByName(read_me)

    def retranslateUi(self, read_me):
        _translate = QtCore.QCoreApplication.translate
        read_me.setWindowTitle(_translate("read_me", "read me"))
        self.plainTextEdit.setPlainText(_translate("read_me", "本工具的功能及使用方法如下：\n"
"1.设定一个目标文件夹（可以在settings里进行默认设置）并输入您想要在ArrayExpress上进行搜索的关键词*。点击search按钮，程序将开始搜集并下载相关的数据，并在您指定的文件夹下生成一个以您输入的关键字命名的txt文档，其中包含了已经经过筛选的数据。在数据下载完毕后，点击open file按钮，选择文件展示其内容至列表中。点击export to excel file按钮可在您选择的文件夹下生成一个excel文档，便于您的浏览和进一步操作。\n"
"2.在下载一个较大的文件时，有小概率会因为短时间内对ArrayExpress请求过多而被阻挡。本工具支持文档的断点续传，请重启程序并增加休息的秒数来避免此种情况，对应下载速度会略为降低。请注意，本工具的所有功能，包括断点续传都是基于文档的名称进行的。如果您想要继续被中断的下载或是更新已下载的数据，请保证选择的文件夹位置和搜索关键词与之前完全一致。同样的，对于已下载的文件更改名称或更换位置将使其不可更新（除非将文件名称改回原样并将当前所在文件夹改为默认文件夹）。\n"
"3.若您有任何问题或建议，请联系我：zengpgh@mail2.sysu.edu.cn\n"
"*搜索的规则参见：https://www.ebi.ac.uk/arrayexpress/help/how_to_search.html#AdvancedSearchExperiment\n"
""))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ArrayFetch = QtWidgets.QMainWindow()
    ui = Ui_ArrayFetch()
    ui.setupUi(ArrayFetch)
    ArrayFetch.show()

    read_me = QtWidgets.QDialog()
    ui2 = Ui_read_me()
    ui2.setupUi(read_me)

    ui.actionhelp.triggered.connect(read_me.show)
    sys.exit(app.exec_())
