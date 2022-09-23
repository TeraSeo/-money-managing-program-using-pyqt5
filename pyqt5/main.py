import sys
from turtle import color
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton,QLineEdit,QLabel, QComboBox,QTableWidget,QTableWidgetItem,QGridLayout
from PyQt5.QtGui import QFont
from PyQt5 import QtCore
import pandas as pd
from PyQt5.QtWidgets import QMessageBox
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt5 import QtCore
from PyQt5.QtChart import QChart,QPieSeries,QChartView
from PyQt5 import QtChart
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys

class Main(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("가계부 정리 프로그램")
        self.setGeometry(50, 50, 1400, 800)
        self.initUI()
        self.trans_list = []
        self.whole_btn_clicked = True

        try:
            self.dataset = pd.read_csv('data.csv', encoding='utf-8')
            self.df = pd.DataFrame(data = self.dataset.values,columns = ['거래 일자', '거래 구분', '거래 금액', '상세 내역', '비고'])
            self.table.setRowCount(len(self.dataset) + 1)
            for i in range(len(self.dataset)):
                self.table.setItem(i,0, QTableWidgetItem(str(self.df.iloc[i,0])))
                self.table.setItem(i,1, QTableWidgetItem(self.df.iloc[i,1]))
                self.table.setItem(i,2, QTableWidgetItem(str(self.df.iloc[i,2])))
                self.table.setItem(i,3, QTableWidgetItem(self.df.iloc[i,3]))
                self.table.setItem(i,4, QTableWidgetItem(str(self.df.iloc[i,4])))

        except pd.errors.EmptyDataError:
            self.df = pd.DataFrame(columns = ['거래 일자', '거래 구분', '거래 금액', '상세 내역', '비고'])
            print('Empty csv file!')

        
    def initUI(self):
        
        #거래 정보창
        self.table_clicked_j = False
        self.trans_date_label = QLabel('거래 일자', self)
        self.trans_date_label.setGeometry(20,25,70,40)

        self.datetime = QDate.currentDate() 
        self.date_textbox = QLineEdit(self)
        self.date_textbox.setGeometry(100,30,120,30)
        self.date_textbox.setAlignment(QtCore.Qt.AlignRight)
        self.date_textbox.setText(self.datetime.toString(Qt.ISODate))

        self.trans_amount_label = QLabel('거래 금액', self)
        self.trans_amount_label.setGeometry(20,85,70,40)
        self.amount_textbox = QLineEdit(self)
        self.amount_textbox.setGeometry(100,90, 120,30)
        self.amount_textbox.setValidator(QIntValidator())
        self.amount_textbox.setMaxLength(10)
        self.amount_textbox.setAlignment(QtCore.Qt.AlignRight)

        self.trans_selec_label = QLabel('거래 구분',self)
        self.trans_selec_label.setGeometry(250,25,70,40)

        self.btn_1 = QComboBox(self)
        self.btn_1.addItem('수입/지출')
        self.btn_1.addItem('수입')
        self.btn_1.addItem('지출')
        
        self.btn_1.activated[str].connect(self.btn_1_clicked)
        self.btn_1.setGeometry(330, 30,170,30)
        self.btn_1.setStyleSheet("background-color: white")
        
        self.trans_label = QLabel('상세 내역', self)
        self.trans_label.setGeometry(250,85,70,40)
        self.btn_2 = QComboBox(self)
        self.btn_2.setGeometry(330,90,170,30)
        self.btn_2.setStyleSheet("background-color: white")
        self.btn_2.addItem('상세 내역')
        
        self.note_label = QLabel('비고', self)
        self.note_label.setGeometry(20,130,70,40)
        

        self.note_textbox = QLineEdit(self)
        self.note_textbox.setGeometry(100,135,400,90)
        self.note_textbox.setAlignment(QtCore.Qt.AlignTop)
        self.note_textbox.setMaxLength(25)

        self.regis_btn = QPushButton('등록',self)
        self.regis_btn.setGeometry(20,245,105,30)
        self.regis_btn.clicked.connect(self.regis_btn_clicked)
    
        self.modify_btn = QPushButton('수정',self)
        self.modify_btn.setGeometry(145,245,105,30)
        self.modify_btn.clicked.connect(self.modify_clicked)

        self.delete_btn = QPushButton('삭제',self)
        self.delete_btn.setGeometry(270,245,105,30)
        self.delete_btn.clicked.connect(self.delete_clicked)

        self.clear_btn = QPushButton('초기화',self)
        self.clear_btn.setGeometry(395,245,105,30)
        self.clear_btn.clicked.connect(self.reset_btn)

        self.income_check_btn = QPushButton('수입 내역 조회', self)
        self.income_check_btn.setGeometry(20,290,230,30)
        self.income_check_btn.clicked.connect(self.in_check)

        self.expense_check_btn = QPushButton('지출 내역 조회', self)
        self.expense_check_btn.setGeometry(270,290,230,30)
        self.expense_check_btn.clicked.connect(self.out_check)

        self.whole_check_btn = QPushButton('전체 내역 조회', self)
        self.whole_check_btn.setGeometry(20,335,480,30)
        self.whole_check_btn.clicked.connect(self.whole_check)

        #데이터 조회

        self.check_label = QLabel('데이터 조회',self)
        self.check_label.setGeometry(540,25,100,40)
        self.check_label.setFont(QFont('Bold',10))

        self.table = QTableWidget(self)
        self.table.setRowCount(self.table.rowCount() + 1)
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(['거래 일자', '거래 구분', '거래 금액', '상세 내역', '비고'])
        self.table.setColumnWidth(0,150)
        self.table.setColumnWidth(1,120)
        self.table.setColumnWidth(2,120)
        self.table.setColumnWidth(3,180)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setGeometry(540,85,820,280)

        self.table.cellClicked.connect(self.table_clicked)

        f = Figure(figsize=(5,4))
        self.canvas = FigureCanvas(f)
        
        self.canvas.setGeometry(50,470,1400,500)

        self.widget = QWidget(self.canvas)
        self.income_chart = QPushButton("수입 차트", self.canvas)
        self.outcome_chart = QPushButton('지출 차트', self.canvas)
        self.compare_chart = QPushButton("비교 차트", self.canvas)
        self.income_chart.setGeometry(20,20,130,40)
        self.outcome_chart.setGeometry(20,90,130,40)
        self.compare_chart.setGeometry(20,160,130,40)
        self.income_chart.clicked.connect(self.income_cal)
        self.outcome_chart.clicked.connect(self.outcome_cal)
        self.compare_chart.clicked.connect(self.compare_cal)

        self.in_1_txt = QLabel(self.canvas)
        self.in_1_txt.setGeometry(1050,20,200,40)

        self.in_2_txt = QLabel(self.canvas)
        self.in_2_txt.setGeometry(1050,80,200,40)

        self.in_3_txt = QLabel(self.canvas)
        self.in_3_txt.setGeometry(1050,140,200,40)

        self.in_4_txt = QLabel(self.canvas)
        self.in_4_txt.setGeometry(1050,200,200,40)

        self.in_5_txt = QLabel(self.canvas)
        self.in_5_txt.setGeometry(1050,260,200,40)

        self.in_6_txt = QLabel(self.canvas)
        self.in_6_txt.setGeometry(1050,320,200,40)

        self.in_7_txt = QLabel(self.canvas)
        self.in_7_txt.setGeometry(1050,380,200,40)

        self.in_8_txt = QLabel(self.canvas)
        self.in_8_txt.setGeometry(1050,440,200,40)

        self.layout = QGridLayout()
 
        self.widget.setLayout(self.layout)

        self.widget.setGeometry(200,0,800,500)
        self.show()   
        self.canvas.setWindowTitle("chart")
        self.canvas.show()

    def regis_btn_clicked(self):    # 등록 버튼에 관한 코드
        self.trans_list = []
        self.table_clicked_j = False

        if not self.whole_btn_clicked:
            QMessageBox.about(self, "Title", "전체 조회를 눌러주세요")

        if self.amount_textbox.text() != "" and self.date_textbox.text() != "" and self.whole_btn_clicked:
            if self.note_textbox.text() != "":
                self.trans_list = []
                self.trans_list.append(self.date_textbox.text())
                self.trans_list.append(self.btn_1.currentText())
                self.trans_list.append(self.amount_textbox.text())
                self.trans_list.append(self.btn_2.currentText())
                self.trans_list.append(self.note_textbox.text())
                self.table.setItem(self.table.rowCount() - 1,0, QTableWidgetItem(self.date_textbox.text()))
                self.table.setItem(self.table.rowCount() - 1,1, QTableWidgetItem(self.btn_1.currentText()))
                self.table.setItem(self.table.rowCount() - 1,2, QTableWidgetItem(self.amount_textbox.text()))
                self.table.setItem(self.table.rowCount() - 1,3, QTableWidgetItem(self.btn_2.currentText()))
                self.table.setItem(self.table.rowCount() - 1,4, QTableWidgetItem(self.note_textbox.text()))
            else:
                self.trans_list = []
                self.trans_list.append(self.date_textbox.text())
                self.trans_list.append(self.btn_1.currentText())
                self.trans_list.append(self.amount_textbox.text())
                self.trans_list.append(self.btn_2.currentText())
                self.trans_list.append("none")
                self.table.setItem(self.table.rowCount() - 1,0, QTableWidgetItem(self.date_textbox.text()))
                self.table.setItem(self.table.rowCount() - 1,1, QTableWidgetItem(self.btn_1.currentText()))
                self.table.setItem(self.table.rowCount() - 1,2, QTableWidgetItem(self.amount_textbox.text()))
                self.table.setItem(self.table.rowCount() - 1,3, QTableWidgetItem(self.btn_2.currentText()))
                self.table.setItem(self.table.rowCount() - 1,4, QTableWidgetItem(self.note_textbox.text()))
        if len(self.trans_list) == 5:
           
            try:
                self.dataset = pd.read_csv('data.csv')
                self.dataset.loc[self.table.rowCount() - 1] = self.trans_list
                self.dataset.to_csv('data.csv', index=False,header = ['거래 일자', '거래 구분', '거래 금액', '상세 내역', '비고'],encoding='utf_8_sig')
            except pd.errors.EmptyDataError:
                self.df.loc[self.table.rowCount() - 1] = self.trans_list
                self.df.to_csv('data.csv', index=False,header = ['거래 일자', '거래 구분', '거래 금액', '상세 내역', '비고'],encoding='utf_8_sig')
                print('Empty csv file!')

            self.trans_list = []
            self.date_textbox.setText(self.datetime.toString(Qt.ISODate))
            self.btn_1.setCurrentText("수입/지출")
            self.amount_textbox.setText("")
            self.btn_2.clear()
            self.btn_2.addItem('거래 내역')
            self.note_textbox.setText("")
            self.table.setRowCount(self.table.rowCount() + 1)
        
    def btn_1_clicked(self,text):
        self.trans_amount_label.setText(text + ' 금액')
        if text == '수입':
            self.btn_2.clear()
            self.btn_2.addItem('이자')
            self.btn_2.addItem('배당')
            self.btn_2.addItem('급여')
            self.btn_2.addItem('기타')
        elif text == '지출':
            self.btn_2.clear()
            self.btn_2.addItem('식대')
            self.btn_2.addItem('의류')
            self.btn_2.addItem('간식')
            self.btn_2.addItem('여가 생활')
            self.btn_2.addItem('보험')
            self.btn_2.addItem('자기 계발')
            self.btn_2.addItem('기타')
        else: 
            self.btn_2.clear()
            self.btn_2.addItem('거래 내역')
    
    def table_clicked(self):
        if not self.whole_btn_clicked:
            QMessageBox.about(self, "Title", "전체 조회를 눌러주세요")
        
        if self.table.currentRow() < self.table.rowCount() - 1 and self.whole_btn_clicked:
            self.table_clicked_j = True
            self.date_textbox.setText(self.table.item(self.table.currentRow(), 0).text())      #############################
            self.btn_1.setCurrentText(self.table.item(self.table.currentRow(), 1).text())
            self.amount_textbox.setText(self.table.item(self.table.currentRow(), 2).text())
            self.btn_2.addItem(self.table.item(self.table.currentRow(), 3).text())
            self.btn_2.addItem('식대')
            self.btn_2.addItem('의류')
            self.btn_2.addItem('간식')
            self.btn_2.addItem('여가 생활')
            self.btn_2.addItem('보험')
            self.btn_2.addItem('자기 계발')
            self.btn_2.addItem('기타')
            self.btn_2.addItem('이자')
            self.btn_2.addItem('배당')
            self.btn_2.addItem('급여')
            self.btn_2.addItem('기타')
            self.note_textbox.setText(self.table.item(self.table.currentRow(), 4).text())

    def modify_clicked(self):   # 수정 버튼에 관한 코드
        
        if not self.whole_btn_clicked:
            QMessageBox.about(self, "Title", "전체 조회를 눌러주세요")

        if self.table_clicked_j and self.whole_btn_clicked:
           
            self.table.setItem(self.table.currentRow(),0, QTableWidgetItem(self.date_textbox.text()))    ###################
            self.table.setItem(self.table.currentRow(),1, QTableWidgetItem(self.btn_1.currentText()))
            self.table.setItem(self.table.currentRow(),2, QTableWidgetItem(self.amount_textbox.text()))
            self.table.setItem(self.table.currentRow(),3, QTableWidgetItem(self.btn_2.currentText()))
            self.table.setItem(self.table.currentRow(),4, QTableWidgetItem(self.note_textbox.text())) 
            
            try:
                self.dataset = pd.read_csv('data.csv')
                self.dataset.loc[self.table.currentRow(), :] = [self.date_textbox.text(),self.btn_1.currentText(),self.amount_textbox.text(),self.btn_2.currentText(),self.note_textbox.text()]
                self.dataset.to_csv('data.csv', index=False,header = ['거래 일자', '거래 구분', '거래 금액', '상세 내역', '비고'],encoding='utf_8_sig')
            except pd.errors.EmptyDataError:
                self.df.loc[self.table.currentRow(), :] = [self.date_textbox.text(),self.btn_1.currentText(),self.amount_textbox.text(),self.btn_2.currentText(),self.note_textbox.text()]
                self.df.to_csv('data.csv', index=False,header = ['거래 일자', '거래 구분', '거래 금액', '상세 내역', '비고'],encoding='utf_8_sig')
                print('Empty csv file!')

            self.date_textbox.setText(self.datetime.toString(Qt.ISODate)) ##############################
            self.btn_1.setCurrentText("수입/지출")
            self.amount_textbox.setText("")
            self.btn_2.clear()
            self.btn_2.addItem('거래 내역')
            self.note_textbox.setText("")
            
    def delete_clicked(self):   # 삭제 버튼에 관한 코드
        if not self.whole_btn_clicked:
            QMessageBox.about(self, "Title", "전체 조회를 눌러주세요")
        
        if self.table_clicked_j and self.whole_btn_clicked:

            try:
                self.dataset = pd.read_csv('data.csv')
                self.dataset.loc[self.table.currentRow(), :] = ["0", "0", "0", "0", "0"]
                self.dataset.to_csv('data.csv', index=False,header = ['거래 일자', '거래 구분', '거래 금액', '상세 내역', '비고'],encoding='utf_8_sig')
            except pd.errors.EmptyDataError:
                self.df.loc[self.table.currentRow(), :] = [self.date_textbox.text(),self.btn_1.currentText(),self.amount_textbox.text(),self.btn_2.currentText(),self.note_textbox.text()]
                self.df.to_csv('data.csv', index=False,header = ["0", "0", "0", "0", "0"],encoding='utf_8_sig')
                print('Empty csv file!')
           
            self.table.setItem(self.table.currentRow(),0, QTableWidgetItem(""))  ################################
            self.table.setItem(self.table.currentRow(),1, QTableWidgetItem(""))
            self.table.setItem(self.table.currentRow(),2, QTableWidgetItem(""))
            self.table.setItem(self.table.currentRow(),3, QTableWidgetItem(""))
            self.table.setItem(self.table.currentRow(),4, QTableWidgetItem("")) 

            self.date_textbox.setText(self.datetime.toString(Qt.ISODate)) ###################################
            self.btn_1.setCurrentText("수입/지출")
            self.amount_textbox.setText("")
            self.btn_2.clear()
            self.btn_2.addItem('거래 내역')
            self.note_textbox.setText("")

    def reset_btn(self):    # 초기화 버튼에 관한 코드
        self.reset = False
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("정말로 초기화 하시겠습니까? ")
        msg.setWindowTitle("reset")
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

        returnValue = msg.exec()
        if returnValue == QMessageBox.Ok:
            self.reset = True
        if self.reset:
            try:
                self.dataset = pd.read_csv('data.csv')
                self.dataset.drop(self.dataset.columns[:],axis=1, inplace=True)
                self.dataset.to_csv('data.csv', index=False,header = False)
                self.table.setRowCount(1)
                self.table.setItem(0,0, QTableWidgetItem(""))
                self.table.setItem(0,1, QTableWidgetItem(""))
                self.table.setItem(0,2, QTableWidgetItem(""))
                self.table.setItem(0,3, QTableWidgetItem(""))
                self.table.setItem(0,4, QTableWidgetItem("")) 
                sys.exit(app.exec_()) 

            except pd.errors.EmptyDataError:
                print('Empty csv file!') 

    def in_check(self): 
        try:
            self.whole_btn_clicked = False
            self.dataset = pd.read_csv('data.csv')
            self.income = []
            for i in range(len(self.dataset)):
                if self.dataset.iloc[i,1] == "수입":
                    self.income.append(self.dataset.iloc[i,:].values)
            self.table.setRowCount(len(self.income))

            for l in range(len(self.income)):
                self.table.setItem(l,0, QTableWidgetItem(str(self.income[l][0])))
                self.table.setItem(l,1, QTableWidgetItem(self.income[l][1]))
                self.table.setItem(l,2, QTableWidgetItem(str(self.income[l][2])))
                self.table.setItem(l,3, QTableWidgetItem(self.income[l][3]))
                self.table.setItem(l,4, QTableWidgetItem(str(self.income[l][4])))
            self.table.setRowCount(len(self.income) + 1)

            
        except pd.errors.EmptyDataError:
            print('Empty csv file!')
    
    def out_check(self):
        try:
            self.whole_btn_clicked = False
            self.dataset = pd.read_csv('data.csv')
            self.out = []
            for i in range(len(self.dataset)):
                if self.dataset.iloc[i,1] == "지출":
                    self.out.append(self.dataset.iloc[i,:].values)
            self.table.setRowCount(len(self.out))

            for l in range(len(self.out)):
                self.table.setItem(l,0, QTableWidgetItem(str(self.out[l][0])))
                self.table.setItem(l,1, QTableWidgetItem(self.out[l][1]))
                self.table.setItem(l,2, QTableWidgetItem(str(self.out[l][2])))
                self.table.setItem(l,3, QTableWidgetItem(self.out[l][3]))
                self.table.setItem(l,4, QTableWidgetItem(str(self.out[l][4])))
            self.table.setRowCount(len(self.out) + 1)
            
        except pd.errors.EmptyDataError:
            print('Empty csv file!')
    def whole_check(self):
        self.whole_btn_clicked = True 
        try:
            self.dataset = pd.read_csv('data.csv')
            self.whole = []
            for i in range(len(self.dataset)):
                self.whole.append(self.dataset.iloc[i,:].values)
            self.table.setRowCount(len(self.whole))

            for l in range(len(self.whole)):
                self.table.setItem(l,0, QTableWidgetItem(str(self.whole[l][0])))
                self.table.setItem(l,1, QTableWidgetItem(self.whole[l][1]))
                self.table.setItem(l,2, QTableWidgetItem(str(self.whole[l][2])))
                self.table.setItem(l,3, QTableWidgetItem(self.whole[l][3]))
                self.table.setItem(l,4, QTableWidgetItem(str(self.whole[l][4])))
            self.table.setRowCount(len(self.whole) + 1)
        except pd.errors.EmptyDataError:
            print('Empty csv file!')

    def income_cal(self):
        try:
            sector_list = ['이자','배당','급여','기타']
            self.income_list = [0,0,0,0]
            self.dataset = pd.read_csv('data.csv')
            whole = self.dataset.iloc[:,:].values
            for i in range(len(whole)):
                if whole[i][1] == '수입':
                    print(whole[i][3])
                    if whole[i][3] in sector_list:
                        k = sector_list.index(whole[i][3])
                        self.income_list[k] += int(whole[i][2])

            
            series = QPieSeries()
            for i in range(len(sector_list)):
                series.append(sector_list[i], self.income_list[i])

            series.setLabelsVisible(True)

            chart = QChart()
            chart.addSeries(series)  
            chart.setAnimationOptions(QChart.SeriesAnimations)
            chartview = QChartView(chart)
            self.layout.addWidget(chartview, 0,0,0,0)
            self.widget.setGeometry(200,0,800,500)

            series.setLabelsPosition(QtChart.QPieSlice.LabelInsideHorizontal)
            for slice in series.slices():
                slice.setLabel("{:.2f}%".format(100 * slice.percentage()))

            for i in range(len(sector_list)):
                chart.legend().markers(series)[i].setLabel(sector_list[i])       

            self.in_1_txt.setText('총 수입 : ' + str(sum(self.income_list)) + '원')
            self.in_2_txt.setText('이자 : ' + str(self.income_list[0]) + '원')
            self.in_3_txt.setText('배당 : ' + str(self.income_list[1]) + '원')
            self.in_4_txt.setText('급여 : ' + str(self.income_list[2]) + '원')
            self.in_5_txt.setText('기타 : ' + str(self.income_list[3]) +'원')
            self.in_6_txt.setText("")
            self.in_7_txt.setText("")
            self.in_8_txt.setText("")

        except pd.errors.EmptyDataError:
            print('Empty csv file!')

    def outcome_cal(self):
        print("outcome")

        try:
            sector_list = ['식대','의류','간식','여가 생활','보험','자기 계발','기타']
            self.outcome_list = [0,0,0,0,0,0,0]
            self.dataset = pd.read_csv('data.csv')
            whole = self.dataset.iloc[:,:].values
            for i in range(len(whole)):
                if whole[i][1] == '지출':
                    if whole[i][3] in sector_list:
                        k = sector_list.index(whole[i][3])
                        self.outcome_list[k] += int(whole[i][2])
                        
            series = QPieSeries()
            for i in range(len(sector_list)):
                series.append(sector_list[i], self.outcome_list[i])
            series.setLabelsVisible(True)

            chart = QChart()
            chart.addSeries(series)  
            chart.setAnimationOptions(QChart.SeriesAnimations)
            chartview = QChartView(chart)
            self.layout.addWidget(chartview, 0,0,0,0)
            self.widget.setGeometry(200,0,800,500)

            series.setLabelsPosition(QtChart.QPieSlice.LabelInsideHorizontal)
            for slice in series.slices():
                slice.setLabel("{:.2f}%".format(100 * slice.percentage()))

            for i in range(len(sector_list)):
                chart.legend().markers(series)[i].setLabel(sector_list[i]) 


            self.in_1_txt.setText('총 지출 : ' + str(sum(self.outcome_list)) + '원')
            self.in_2_txt.setText('식대 : ' + str(self.outcome_list[0]) + '원')
            self.in_3_txt.setText('의류 : ' + str(self.outcome_list[1]) + '원')
            self.in_4_txt.setText('간식 : ' + str(self.outcome_list[2]) + '원')
            self.in_5_txt.setText('여가 생활 : ' + str(self.outcome_list[3]) +'원')
            self.in_6_txt.setText('보험 : ' + str(self.outcome_list[4]) + '원')
            self.in_7_txt.setText('자기 계발 : ' + str(self.outcome_list[5]) + '원')
            self.in_8_txt.setText('기타 : ' + str(self.outcome_list[6]) + '원')
        
        except pd.errors.EmptyDataError:
            print('Empty csv file!')

    def compare_cal(self):
        print("compare")

        try:
            out_sector_list = ['식대','의류','간식','여가 생활','보험','자기 계발','기타']
            self.outcome_list = [0,0,0,0,0,0,0]
            self.dataset = pd.read_csv('data.csv')
            whole = self.dataset.iloc[:,:].values
            for i in range(len(whole)):
                if whole[i][1] == '지출':
                    if whole[i][3] in out_sector_list:
                        k = out_sector_list.index(whole[i][3])
                        self.outcome_list[k] += int(whole[i][2])
            
            in_sector_list = ['이자','배당','급여','기타']
            self.income_list = [0,0,0,0]
            self.dataset = pd.read_csv('data.csv')
            whole = self.dataset.iloc[:,:].values
            for i in range(len(whole)):
                if whole[i][1] == '수입':
                    print(whole[i][3])
                    if whole[i][3] in in_sector_list:
                        k = in_sector_list.index(whole[i][3])
                        #income_list[k] += income_list[i]
                        self.income_list[k] += int(whole[i][2])
            series = QPieSeries()
            series.append("총 수입", sum(self.income_list))
            series.append("총 지출", sum(self.outcome_list))
            series.setLabelsVisible(True)

            chart = QChart()
            chart.addSeries(series)  
            chart.setAnimationOptions(QChart.SeriesAnimations)
            chartview = QChartView(chart)
            self.layout.addWidget(chartview, 0,0,0,0)
            self.widget.setGeometry(200,0,800,500)

            series.setLabelsPosition(QtChart.QPieSlice.LabelInsideHorizontal)
            for slice in series.slices():
                slice.setLabel("{:.2f}%".format(100 * slice.percentage()))

            chart.legend().markers(series)[0].setLabel("총 수입") 
            chart.legend().markers(series)[1].setLabel("총 지출")
        
        except pd.errors.EmptyDataError:
            print('Empty csv file!')


        self.in_1_txt.setText('총 수입 : ' + str(sum(self.income_list)) + '원')
        self.in_2_txt.setText('총 지출 : ' + str(sum(self.outcome_list)) + '원')
        self.in_3_txt.setText("")
        self.in_4_txt.setText("")
        self.in_5_txt.setText("")
        self.in_6_txt.setText("")
        self.in_7_txt.setText("")
        self.in_8_txt.setText("")


app = QApplication(sys.argv)
main = Main()
sys.exit(app.exec_())  # 이벤트 처리를 위한 메인 루프