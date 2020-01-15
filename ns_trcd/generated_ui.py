# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ns_app.ui',
# licensing of 'ns_app.ui' applies.
#
# Created: Sun Jan 12 16:40:25 2020
#      by: pyside2-uic  running on PySide2 5.12.6
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(723, 572)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.tabs = QtWidgets.QTabWidget(self.centralwidget)
        self.tabs.setObjectName("tabs")
        self.live_tab = QtWidgets.QWidget()
        self.live_tab.setObjectName("live_tab")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.live_tab)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.scrollArea = QtWidgets.QScrollArea(self.live_tab)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 577, 1316))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.live_par_label = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.live_par_label.sizePolicy().hasHeightForWidth()
        )
        self.live_par_label.setSizePolicy(sizePolicy)
        self.live_par_label.setObjectName("live_par_label")
        self.verticalLayout.addWidget(self.live_par_label)
        self.live_par_graph = PlotWidget(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.live_par_graph.sizePolicy().hasHeightForWidth()
        )
        self.live_par_graph.setSizePolicy(sizePolicy)
        self.live_par_graph.setObjectName("live_par_graph")
        self.verticalLayout.addWidget(self.live_par_graph)
        self.live_perp_label = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.live_perp_label.setObjectName("live_perp_label")
        self.verticalLayout.addWidget(self.live_perp_label)
        self.live_perp_graph = PlotWidget(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.live_perp_graph.sizePolicy().hasHeightForWidth()
        )
        self.live_perp_graph.setSizePolicy(sizePolicy)
        self.live_perp_graph.setObjectName("live_perp_graph")
        self.verticalLayout.addWidget(self.live_perp_graph)
        self.live_ref_label = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.live_ref_label.setObjectName("live_ref_label")
        self.verticalLayout.addWidget(self.live_ref_label)
        self.live_ref_graph = PlotWidget(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.live_ref_graph.sizePolicy().hasHeightForWidth()
        )
        self.live_ref_graph.setSizePolicy(sizePolicy)
        self.live_ref_graph.setObjectName("live_ref_graph")
        self.verticalLayout.addWidget(self.live_ref_graph)
        self.live_par_da_label = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.live_par_da_label.setObjectName("live_par_da_label")
        self.verticalLayout.addWidget(self.live_par_da_label)
        self.live_par_da_graph = PlotWidget(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.live_par_da_graph.sizePolicy().hasHeightForWidth()
        )
        self.live_par_da_graph.setSizePolicy(sizePolicy)
        self.live_par_da_graph.setObjectName("live_par_da_graph")
        self.verticalLayout.addWidget(self.live_par_da_graph)
        self.live_perp_da_label = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.live_perp_da_label.setObjectName("live_perp_da_label")
        self.verticalLayout.addWidget(self.live_perp_da_label)
        self.live_perp_da_graph = PlotWidget(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.live_perp_da_graph.sizePolicy().hasHeightForWidth()
        )
        self.live_perp_da_graph.setSizePolicy(sizePolicy)
        self.live_perp_da_graph.setObjectName("live_perp_da_graph")
        self.verticalLayout.addWidget(self.live_perp_da_graph)
        self.live_cd_label = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.live_cd_label.setObjectName("live_cd_label")
        self.verticalLayout.addWidget(self.live_cd_label)
        self.live_cd_graph = PlotWidget(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.live_cd_graph.sizePolicy().hasHeightForWidth()
        )
        self.live_cd_graph.setSizePolicy(sizePolicy)
        self.live_cd_graph.setObjectName("live_cd_graph")
        self.verticalLayout.addWidget(self.live_cd_graph)
        self.verticalLayout_7.addLayout(self.verticalLayout)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout_2.addWidget(self.scrollArea)
        self.tabs.addTab(self.live_tab, "")
        self.average_tab = QtWidgets.QWidget()
        self.average_tab.setObjectName("average_tab")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.average_tab)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.scrollArea_2 = QtWidgets.QScrollArea(self.average_tab)
        self.scrollArea_2.setWidgetResizable(True)
        self.scrollArea_2.setObjectName("scrollArea_2")
        self.scrollAreaWidgetContents_2 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_2.setGeometry(QtCore.QRect(0, 0, 594, 465))
        self.scrollAreaWidgetContents_2.setObjectName("scrollAreaWidgetContents_2")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents_2)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.avg_par_da_label = QtWidgets.QLabel(self.scrollAreaWidgetContents_2)
        self.avg_par_da_label.setObjectName("avg_par_da_label")
        self.verticalLayout_3.addWidget(self.avg_par_da_label)
        self.avg_par_da_graph = PlotWidget(self.scrollAreaWidgetContents_2)
        self.avg_par_da_graph.setObjectName("avg_par_da_graph")
        self.verticalLayout_3.addWidget(self.avg_par_da_graph)
        self.avg_perp_da_label = QtWidgets.QLabel(self.scrollAreaWidgetContents_2)
        self.avg_perp_da_label.setObjectName("avg_perp_da_label")
        self.verticalLayout_3.addWidget(self.avg_perp_da_label)
        self.avg_perp_da_graph = PlotWidget(self.scrollAreaWidgetContents_2)
        self.avg_perp_da_graph.setObjectName("avg_perp_da_graph")
        self.verticalLayout_3.addWidget(self.avg_perp_da_graph)
        self.avg_cd_label = QtWidgets.QLabel(self.scrollAreaWidgetContents_2)
        self.avg_cd_label.setObjectName("avg_cd_label")
        self.verticalLayout_3.addWidget(self.avg_cd_label)
        self.avg_cd_graph = PlotWidget(self.scrollAreaWidgetContents_2)
        self.avg_cd_graph.setObjectName("avg_cd_graph")
        self.verticalLayout_3.addWidget(self.avg_cd_graph)
        self.verticalLayout_8.addLayout(self.verticalLayout_3)
        self.scrollArea_2.setWidget(self.scrollAreaWidgetContents_2)
        self.verticalLayout_4.addWidget(self.scrollArea_2)
        self.tabs.addTab(self.average_tab, "")
        self.horizontalLayout.addWidget(self.tabs)
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.start_btn = QtWidgets.QPushButton(self.centralwidget)
        self.start_btn.setObjectName("start_btn")
        self.verticalLayout_5.addWidget(self.start_btn)
        self.stop_btn = QtWidgets.QPushButton(self.centralwidget)
        self.stop_btn.setObjectName("stop_btn")
        self.verticalLayout_5.addWidget(self.stop_btn)
        self.horizontalLayout.addLayout(self.verticalLayout_5)
        self.verticalLayout_6.addLayout(self.horizontalLayout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 723, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.tabs.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(
            QtWidgets.QApplication.translate("MainWindow", "MainWindow", None, -1)
        )
        self.live_par_label.setText(
            QtWidgets.QApplication.translate("MainWindow", "Parallel", None, -1)
        )
        self.live_perp_label.setText(
            QtWidgets.QApplication.translate("MainWindow", "Perpendicular", None, -1)
        )
        self.live_ref_label.setText(
            QtWidgets.QApplication.translate("MainWindow", "Reference", None, -1)
        )
        self.live_par_da_label.setText(
            QtWidgets.QApplication.translate("MainWindow", "Parallel - dA", None, -1)
        )
        self.live_perp_da_label.setText(
            QtWidgets.QApplication.translate(
                "MainWindow", "Perpendicular - dA", None, -1
            )
        )
        self.live_cd_label.setText(
            QtWidgets.QApplication.translate("MainWindow", "CD", None, -1)
        )
        self.tabs.setTabText(
            self.tabs.indexOf(self.live_tab),
            QtWidgets.QApplication.translate("MainWindow", "Live", None, -1),
        )
        self.avg_par_da_label.setText(
            QtWidgets.QApplication.translate("MainWindow", "Parallel", None, -1)
        )
        self.avg_perp_da_label.setText(
            QtWidgets.QApplication.translate("MainWindow", "Perpendicular", None, -1)
        )
        self.avg_cd_label.setText(
            QtWidgets.QApplication.translate("MainWindow", "CD", None, -1)
        )
        self.tabs.setTabText(
            self.tabs.indexOf(self.average_tab),
            QtWidgets.QApplication.translate("MainWindow", "Average", None, -1),
        )
        self.start_btn.setText(
            QtWidgets.QApplication.translate("MainWindow", "Start", None, -1)
        )
        self.stop_btn.setText(
            QtWidgets.QApplication.translate("MainWindow", "Stop", None, -1)
        )


from pyqtgraph import PlotWidget
