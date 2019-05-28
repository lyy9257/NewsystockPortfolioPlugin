# coding=utf-8
import sys
from PyQt5 import QtWidgets
from PyQt5 import uic
from PyQt5.QtGui import QPixmap

import time

import portfolio_optimize

class Form(QtWidgets.QDialog):
    def __init__(self, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self.ui = uic.loadUi("front.ui", self)

        self.sharp_simulate = portfolio_optimize.set_pf_weight()
        self.predict_amount = portfolio_optimize.simulate_amount_graph()
        
        ## 시뮬레이션 버튼
        self.StartSimulation.clicked.connect(self.simulation)
    
        ## 그래프 출력 버튼
        self.ShowSharpGraph.clicked.connect(self.show_graph_sharp_simulation)
        self.ShowEquityCurve.clicked.connect(self.show_graph_asset_growth)
    

    ## 샤프 시뮬레이션 버튼 클릭시 작동
    def simulation(self):

        ## 입력 포트폴리오 번호 확인
        pf_str = self.ReadPFlist.text()
        
        ## 포트폴리오 갯수 출력
        pf_list = self.sharp_simulate.read_pf(pf_str)

        if len(pf_list) < 6:
            self.ShowPFAmount.setText(str(len(pf_list)))
        
            ## 샤프비 시뮬레이션
            processd_data = self.sharp_simulate.preprocess_tradedata()
            simulated_data = self.sharp_simulate.get_random_pf_weight(processd_data)
            self.sharp_simulate.draw_graph_sharp_ratio(simulated_data)
        
            ## 수익률 커브 시뮬레이션
            self.predict_amount.read_pf(pf_str)
            processed_tradedata = self.predict_amount.preprocess_tradedata(simulated_data)
            self.predict_amount.draw_graph(processed_tradedata)

            ## 성과 출력
            result_sharp = self.sharp_simulate.get_result(simulated_data) 
            result_account = self.predict_amount.get_result(processed_tradedata)

            self.resultlogbox.insertPlainText("[시뮬레이션 결과] \n")
            self.resultlogbox.insertPlainText("예상 수익률 : %.3f %% \n" %(result_sharp[0] * 100))
            self.resultlogbox.insertPlainText("예상 변동성 : %.3f %% \n" %(result_sharp[1] * 100))
            self.resultlogbox.insertPlainText("예상 샤프비 : %.3f \n\n" %result_sharp[2])

            for k in range(len(pf_list)):
                self.resultlogbox.insertPlainText("%s 포트 비중 : %.3f %% \n" %(pf_list[k], result_sharp[k+3] * 100))

            self.resultlogbox.insertPlainText("\n예상 CAGR : %.3f %%\n" %result_account[0]) 
            self.resultlogbox.insertPlainText("예상 MDD : %.3f %%\n\n" %result_account[1])   

            return True
    
        else:
            self.ShowPFAmount.setText("포트 갯수 초과")
            return False

    ## 샤프비 시뮬레이션 그래프 출력
    def show_graph_sharp_simulation(self):
        pixmap = QPixmap("sharp_simulate.png")
        pixmap = pixmap.scaledToWidth(700)
            
        self.ShowGraphImage.setPixmap(pixmap)

    
    ## 수익률 커브 그래프 출력
    def show_graph_asset_growth(self):
        pixmap = QPixmap("Genport_Curve_and_MDD_Simulation")
        pixmap = pixmap.scaledToWidth(700)
            
        self.ShowGraphImage.setPixmap(pixmap)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Form()
    window.show()
    sys.exit(app.exec())