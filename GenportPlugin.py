#-*- coding:utf-8 -*-

import sys
from PyQt5 import QtWidgets
from PyQt5 import uic
from PyQt5.QtGui import QPixmap

import time

import handler

class Form(QtWidgets.QDialog):
    def __init__(self, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self.ui = uic.loadUi("front.ui", self)

        self.simulation_onetime = handler.onetime_sharp_simulation()
        self.simulation_month = handler.month_sharp_simulation()
        
        '''
        단독 시뮬레이션 키 커넥트
        '''
             
        ## 시뮬레이션 버튼_단독
        self.StartSimulation.clicked.connect(self.onetime_connect)
    
        ## 그래프 출력 버튼_단독
        self.ShowSharpGraph.clicked.connect(self.show_sharp)
        self.ShowCurve.clicked.connect(self.show_curve)
        self.ShowMDD.clicked.connect(self.show_mdd)

        '''
        월별 시뮬레이션 키 커넥트
        '''

        ## 시뮬레이션 버튼_월별
        self.StartSimulation_month.clicked.connect(self.month_connect)
    
        ## 그래프 출력 버튼_월별
        self.ShowCurve_month.clicked.connect(self.show_curve_month)
        self.ShowMDD_month.clicked.connect(self.show_mdd_month)


    '''
    단독 시뮬레이션
    '''

    ## 샤프 시뮬레이션 버튼 클릭시 작동
    def onetime_connect(self):

        ## 입력 포트폴리오 번호 확인
        pf_str = self.ReadPFlist.text()
        
        ## 포트폴리오 갯수 출력
        pf_list = self.simulation_onetime.get_pf_list(pf_str)
        
        if len(pf_list) < 6:
            print('(1/4) Get Portfolio list...')
            self.ShowPFAmount.setText(str(len(pf_list)))
            
            ## 데이터 전처리
            print('(2/4) Preprocessing Portfolio Data...')
            self.simulation_onetime.preprocess_data()

            ## 샤프비 시뮬레이션
            print('(3/4) Simulation...')
            self.simulation_onetime.simulate()
        
            ## 그래프 작도
            print('(4/4) Drawing Graph...\n')
            self.simulation_onetime.draw_graph()

            ## 성과 출력
            result_sharp = self.simulation_onetime.get_sharp_result()
            result_cagr = self.simulation_onetime.get_cagr_result()

            self.resultlogbox.insertPlainText("[시뮬레이션 결과] \n")
            
            ## 사용자에게 혼란을 야기할 수 있어 예상 수익률 및 예상 변동성 출력 제거

            ## self.resultlogbox.insertPlainText("예상 수익률 : %.3f %% \n" %(result_sharp[0] * 100))
            ## self.resultlogbox.insertPlainText("예상 변동성 : %.3f %% \n" %(result_sharp[1] * 100))
            
            self.resultlogbox.insertPlainText("예상 샤프비 : %.3f \n\n" %result_sharp[2])

            for k in range(len(pf_list)):
                self.resultlogbox.insertPlainText("%s 포트 비중 : %.3f %% \n" %(pf_list[k], result_sharp[k+3] * 100))

            self.resultlogbox.insertPlainText("\n예상 CAGR : %.3f %%\n" %result_cagr[0]) 
            self.resultlogbox.insertPlainText("예상 MDD : %.3f %%\n\n" %result_cagr[1])   

            return True
    
        else:
            self.ShowPFAmount.setText("포트 갯수 초과")
            return False


    ## 샤프비 시뮬레이션 그래프 출력
    def show_sharp(self):
        pixmap = QPixmap("Sharp_Simulate.png")
        pixmap = pixmap.scaledToWidth(700)
            
        self.ShowGraphImage.setPixmap(pixmap)

    
    ## 수익률 커브 그래프 출력
    def show_curve(self):
        pixmap = QPixmap("Genport_Curve_Simulation.png")
        pixmap = pixmap.scaledToWidth(700)
            
        self.ShowGraphImage.setPixmap(pixmap)


    ## MDD 그래프 출력
    def show_mdd(self):
        pixmap = QPixmap("Genport_MDD_Simulation.png")
        pixmap = pixmap.scaledToWidth(700)
            
        self.ShowGraphImage.setPixmap(pixmap)


    '''
    월별 시뮬레이션
    '''

    ## 샤프 시뮬레이션 버튼 클릭시 작동
    def month_connect(self):
        
        ## 입력 포트폴리오 번호 확인
        pf_str = self.ReadPFlist_month.text()
        
        ## 포트폴리오 갯수 출력
        pf_list = self.simulation_month.get_pf_list(pf_str)
        
        if len(pf_list) < 6:
            print('(1/4) Get Portfolio list...')
            self.ShowPFAmount_month.setText(str(len(pf_list)))

            ## 데이터 전처리
            print('(2/4) Preprocessing Portfolio Data...')
            self.simulation_month.preprocess_data()
            
            ## 샤프비 시뮬레이션
            print('(3/4) Simulation...')
            self.simulation_month.simulate_()
            
            ## 그래프 작도
            print('(4/4) Drawing Graph...\n')
            self.simulation_month.draw_graph()

            ## 성과 출력
            result_cagr = self.simulation_month.get_cagr_result()

            self.resultlogbox_month.insertPlainText("[시뮬레이션 결과] \n")

            self.resultlogbox_month.insertPlainText("\n예상 CAGR : %.3f %%\n" %result_cagr[0]) 
            self.resultlogbox_month.insertPlainText("예상 MDD : %.3f %%\n\n" %result_cagr[1])   

            self.resultlogbox_month.insertPlainText("[월별 비중파일이 CSV파일로 저장되었습니다.] \n")
            
            return True
            
        else:
            self.ShowPFAmount_month.setText("포트 갯수 초과")
            return False
    

    ## 수익률 커브 그래프 출력
    def show_curve_month(self):
        pixmap = QPixmap("Genport_Curve_Simulation.png")
        pixmap = pixmap.scaledToWidth(700)
            
        self.ShowGraphImage_month.setPixmap(pixmap)


    ## MDD 그래프 출력
    def show_mdd_month(self):
        pixmap = QPixmap("Genport_MDD_Simulation.png")
        pixmap = pixmap.scaledToWidth(700)
            
        self.ShowGraphImage_month.setPixmap(pixmap)



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Form()
    window.show()
    sys.exit(app.exec())
