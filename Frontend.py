import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic

## Back-End Package Loading
import portfoliooptimize

## Form
form_class = uic.loadUiType("front.ui")[0]

class routine():
    def __init__(self):

    def sharp_simulation(self)
        processd_data = Opt_portfolio.preprocess_tradedata()
        simulated_data = Opt_portfolio.random_portfolio_weight(processd_data)
        Opt_portfolio.draw_graph_sharp_ratio(simulated_data)


## 창 시현
class MyWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        Backend_OptPortfolio = portfoliooptimize.Opt_portfolio

        ## 시뮬레이션 시작 버튼
        self.StartSimulation.clicked.connect(self.Start_Simulation)

        ## 그래프 시현버튼
        self.ShowSharpGraph.clicked.connect(self.Show_SharpGraph)
        self.ShowEquityCurve.clicked.connect(self.Show_EquityCurve)


    ## 시뮬레이션 시작 버튼 눌렀을 경우
    def Start_Simulation(self):

        ## 시뮬레이션 전 포트폴리오 확인 및 입력 갯수 출력
        pf_list = self.readPFlist.text()
        pf_amount = Backend_OptPortfolio.read_portfolio(pf_list)
        self.ShowPFAmount.settext(pf_amount)

        ## 1. 샤프비 시뮬레이션

        ## 2. 수익률 커브 시뮬레이션


    ## 샤프비 시뮬 구현
    def Show_SharpGraph(self):


    ## 수익률 커브 시현
    def Show_EquityCurve(self):


## UI 띄우기
if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    app.exec_()

