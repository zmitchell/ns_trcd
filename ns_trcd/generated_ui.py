# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ns_app.ui',
# licensing of 'ns_app.ui' applies.
#
# Created: Thu Feb  6 18:12:37 2020
#      by: pyside2-uic  running on PySide2 5.12.6
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(829, 652)
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
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 683, 2564))
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
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.live_par_graph.sizePolicy().hasHeightForWidth()
        )
        self.live_par_graph.setSizePolicy(sizePolicy)
        self.live_par_graph.setMinimumSize(QtCore.QSize(0, 400))
        self.live_par_graph.setObjectName("live_par_graph")
        self.verticalLayout.addWidget(self.live_par_graph)
        self.live_perp_label = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.live_perp_label.setObjectName("live_perp_label")
        self.verticalLayout.addWidget(self.live_perp_label)
        self.live_perp_graph = PlotWidget(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.live_perp_graph.sizePolicy().hasHeightForWidth()
        )
        self.live_perp_graph.setSizePolicy(sizePolicy)
        self.live_perp_graph.setMinimumSize(QtCore.QSize(0, 400))
        self.live_perp_graph.setObjectName("live_perp_graph")
        self.verticalLayout.addWidget(self.live_perp_graph)
        self.live_ref_label = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.live_ref_label.setObjectName("live_ref_label")
        self.verticalLayout.addWidget(self.live_ref_label)
        self.live_ref_graph = PlotWidget(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.live_ref_graph.sizePolicy().hasHeightForWidth()
        )
        self.live_ref_graph.setSizePolicy(sizePolicy)
        self.live_ref_graph.setMinimumSize(QtCore.QSize(0, 400))
        self.live_ref_graph.setObjectName("live_ref_graph")
        self.verticalLayout.addWidget(self.live_ref_graph)
        self.live_par_da_label = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.live_par_da_label.setObjectName("live_par_da_label")
        self.verticalLayout.addWidget(self.live_par_da_label)
        self.live_da_par_graph = PlotWidget(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.live_da_par_graph.sizePolicy().hasHeightForWidth()
        )
        self.live_da_par_graph.setSizePolicy(sizePolicy)
        self.live_da_par_graph.setMinimumSize(QtCore.QSize(0, 400))
        self.live_da_par_graph.setObjectName("live_da_par_graph")
        self.verticalLayout.addWidget(self.live_da_par_graph)
        self.live_perp_da_label = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.live_perp_da_label.setObjectName("live_perp_da_label")
        self.verticalLayout.addWidget(self.live_perp_da_label)
        self.live_da_perp_graph = PlotWidget(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.live_da_perp_graph.sizePolicy().hasHeightForWidth()
        )
        self.live_da_perp_graph.setSizePolicy(sizePolicy)
        self.live_da_perp_graph.setMinimumSize(QtCore.QSize(0, 400))
        self.live_da_perp_graph.setObjectName("live_da_perp_graph")
        self.verticalLayout.addWidget(self.live_da_perp_graph)
        self.live_cd_label = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.live_cd_label.setObjectName("live_cd_label")
        self.verticalLayout.addWidget(self.live_cd_label)
        self.live_da_cd_graph = PlotWidget(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.live_da_cd_graph.sizePolicy().hasHeightForWidth()
        )
        self.live_da_cd_graph.setSizePolicy(sizePolicy)
        self.live_da_cd_graph.setMinimumSize(QtCore.QSize(0, 400))
        self.live_da_cd_graph.setObjectName("live_da_cd_graph")
        self.verticalLayout.addWidget(self.live_da_cd_graph)
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
        self.scrollAreaWidgetContents_2.setGeometry(QtCore.QRect(0, 0, 683, 1289))
        self.scrollAreaWidgetContents_2.setObjectName("scrollAreaWidgetContents_2")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents_2)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.avg_da_par_label = QtWidgets.QLabel(self.scrollAreaWidgetContents_2)
        self.avg_da_par_label.setObjectName("avg_da_par_label")
        self.verticalLayout_3.addWidget(self.avg_da_par_label)
        self.avg_da_par_graph = PlotWidget(self.scrollAreaWidgetContents_2)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.avg_da_par_graph.sizePolicy().hasHeightForWidth()
        )
        self.avg_da_par_graph.setSizePolicy(sizePolicy)
        self.avg_da_par_graph.setMinimumSize(QtCore.QSize(0, 400))
        self.avg_da_par_graph.setObjectName("avg_da_par_graph")
        self.verticalLayout_3.addWidget(self.avg_da_par_graph)
        self.avg_da_perp_label = QtWidgets.QLabel(self.scrollAreaWidgetContents_2)
        self.avg_da_perp_label.setObjectName("avg_da_perp_label")
        self.verticalLayout_3.addWidget(self.avg_da_perp_label)
        self.avg_da_perp_graph = PlotWidget(self.scrollAreaWidgetContents_2)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.avg_da_perp_graph.sizePolicy().hasHeightForWidth()
        )
        self.avg_da_perp_graph.setSizePolicy(sizePolicy)
        self.avg_da_perp_graph.setMinimumSize(QtCore.QSize(0, 400))
        self.avg_da_perp_graph.setObjectName("avg_da_perp_graph")
        self.verticalLayout_3.addWidget(self.avg_da_perp_graph)
        self.avg_da_cd_label = QtWidgets.QLabel(self.scrollAreaWidgetContents_2)
        self.avg_da_cd_label.setObjectName("avg_da_cd_label")
        self.verticalLayout_3.addWidget(self.avg_da_cd_label)
        self.avg_da_cd_graph = PlotWidget(self.scrollAreaWidgetContents_2)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.avg_da_cd_graph.sizePolicy().hasHeightForWidth()
        )
        self.avg_da_cd_graph.setSizePolicy(sizePolicy)
        self.avg_da_cd_graph.setMinimumSize(QtCore.QSize(0, 400))
        self.avg_da_cd_graph.setObjectName("avg_da_cd_graph")
        self.verticalLayout_3.addWidget(self.avg_da_cd_graph)
        self.verticalLayout_8.addLayout(self.verticalLayout_3)
        self.scrollArea_2.setWidget(self.scrollAreaWidgetContents_2)
        self.verticalLayout_4.addWidget(self.scrollArea_2)
        self.tabs.addTab(self.average_tab, "")
        self.acq_tab = QtWidgets.QWidget()
        self.acq_tab.setObjectName("acq_tab")
        self.verticalLayout_9 = QtWidgets.QVBoxLayout(self.acq_tab)
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.instr_name = QtWidgets.QLineEdit(self.acq_tab)
        self.instr_name.setObjectName("instr_name")
        self.gridLayout.addWidget(self.instr_name, 0, 1, 1, 1)
        self.save_data_checkbox = QtWidgets.QCheckBox(self.acq_tab)
        self.save_data_checkbox.setText("")
        self.save_data_checkbox.setObjectName("save_data_checkbox")
        self.gridLayout.addWidget(self.save_data_checkbox, 2, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.acq_tab)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 3, 0, 1, 1)
        self.label = QtWidgets.QLabel(self.acq_tab)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 2, 0, 1, 1)
        self.reset_avg_btn = QtWidgets.QPushButton(self.acq_tab)
        self.reset_avg_btn.setObjectName("reset_avg_btn")
        self.gridLayout.addWidget(self.reset_avg_btn, 6, 1, 1, 1)
        self.measurements = QtWidgets.QSpinBox(self.acq_tab)
        self.measurements.setMinimum(1)
        self.measurements.setMaximum(1000000)
        self.measurements.setProperty("value", 5)
        self.measurements.setObjectName("measurements")
        self.gridLayout.addWidget(self.measurements, 1, 1, 1, 1)
        self.measurements_label = QtWidgets.QLabel(self.acq_tab)
        self.measurements_label.setObjectName("measurements_label")
        self.gridLayout.addWidget(self.measurements_label, 1, 0, 1, 1)
        self.instr_name_label = QtWidgets.QLabel(self.acq_tab)
        self.instr_name_label.setObjectName("instr_name_label")
        self.gridLayout.addWidget(self.instr_name_label, 0, 0, 1, 1)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.save_loc = QtWidgets.QLineEdit(self.acq_tab)
        self.save_loc.setEnabled(False)
        self.save_loc.setObjectName("save_loc")
        self.horizontalLayout_3.addWidget(self.save_loc)
        self.save_loc_browse_btn = QtWidgets.QPushButton(self.acq_tab)
        self.save_loc_browse_btn.setEnabled(True)
        self.save_loc_browse_btn.setObjectName("save_loc_browse_btn")
        self.horizontalLayout_3.addWidget(self.save_loc_browse_btn)
        self.gridLayout.addLayout(self.horizontalLayout_3, 3, 1, 1, 1)
        self.start_pt_label = QtWidgets.QLabel(self.acq_tab)
        self.start_pt_label.setObjectName("start_pt_label")
        self.gridLayout.addWidget(self.start_pt_label, 4, 0, 1, 1)
        self.stop_pt_label = QtWidgets.QLabel(self.acq_tab)
        self.stop_pt_label.setObjectName("stop_pt_label")
        self.gridLayout.addWidget(self.stop_pt_label, 5, 0, 1, 1)
        self.start_pt = QtWidgets.QSpinBox(self.acq_tab)
        self.start_pt.setMinimum(1)
        self.start_pt.setMaximum(249999)
        self.start_pt.setObjectName("start_pt")
        self.gridLayout.addWidget(self.start_pt, 4, 1, 1, 1)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.stop_pt = QtWidgets.QSpinBox(self.acq_tab)
        self.stop_pt.setEnabled(False)
        self.stop_pt.setMinimum(2)
        self.stop_pt.setMaximum(250000)
        self.stop_pt.setProperty("value", 5000)
        self.stop_pt.setObjectName("stop_pt")
        self.horizontalLayout_4.addWidget(self.stop_pt)
        self.stop_pt_checkbox = QtWidgets.QCheckBox(self.acq_tab)
        self.stop_pt_checkbox.setChecked(True)
        self.stop_pt_checkbox.setObjectName("stop_pt_checkbox")
        self.horizontalLayout_4.addWidget(self.stop_pt_checkbox)
        self.gridLayout.addLayout(self.horizontalLayout_4, 5, 1, 1, 1)
        self.horizontalLayout_2.addLayout(self.gridLayout)
        spacerItem = QtWidgets.QSpacerItem(
            200, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
        )
        self.horizontalLayout_2.addItem(spacerItem)
        self.verticalLayout_9.addLayout(self.horizontalLayout_2)
        spacerItem1 = QtWidgets.QSpacerItem(
            20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding
        )
        self.verticalLayout_9.addItem(spacerItem1)
        self.tabs.addTab(self.acq_tab, "")
        self.horizontalLayout.addWidget(self.tabs)
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.measurement_counter_label = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.measurement_counter_label.sizePolicy().hasHeightForWidth()
        )
        self.measurement_counter_label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setWeight(75)
        font.setBold(True)
        self.measurement_counter_label.setFont(font)
        self.measurement_counter_label.setAlignment(QtCore.Qt.AlignCenter)
        self.measurement_counter_label.setObjectName("measurement_counter_label")
        self.verticalLayout_5.addWidget(self.measurement_counter_label)
        self.start_btn = QtWidgets.QPushButton(self.centralwidget)
        self.start_btn.setObjectName("start_btn")
        self.verticalLayout_5.addWidget(self.start_btn)
        self.stop_btn = QtWidgets.QPushButton(self.centralwidget)
        self.stop_btn.setObjectName("stop_btn")
        self.verticalLayout_5.addWidget(self.stop_btn)
        spacerItem2 = QtWidgets.QSpacerItem(
            20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding
        )
        self.verticalLayout_5.addItem(spacerItem2)
        self.horizontalLayout.addLayout(self.verticalLayout_5)
        self.verticalLayout_6.addLayout(self.horizontalLayout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 829, 21))
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
        self.avg_da_par_label.setText(
            QtWidgets.QApplication.translate("MainWindow", "Parallel", None, -1)
        )
        self.avg_da_perp_label.setText(
            QtWidgets.QApplication.translate("MainWindow", "Perpendicular", None, -1)
        )
        self.avg_da_cd_label.setText(
            QtWidgets.QApplication.translate("MainWindow", "CD", None, -1)
        )
        self.tabs.setTabText(
            self.tabs.indexOf(self.average_tab),
            QtWidgets.QApplication.translate("MainWindow", "Average", None, -1),
        )
        self.instr_name.setText(
            QtWidgets.QApplication.translate(
                "MainWindow", "TCPIP::192.168.20.4::gpib0,1::INSTR", None, -1
            )
        )
        self.label_2.setText(
            QtWidgets.QApplication.translate("MainWindow", "Save Location", None, -1)
        )
        self.label.setText(
            QtWidgets.QApplication.translate("MainWindow", "Save Data", None, -1)
        )
        self.reset_avg_btn.setText(
            QtWidgets.QApplication.translate("MainWindow", "Reset Averages", None, -1)
        )
        self.measurements_label.setText(
            QtWidgets.QApplication.translate("MainWindow", "Measurements", None, -1)
        )
        self.instr_name_label.setText(
            QtWidgets.QApplication.translate("MainWindow", "Instrument Name", None, -1)
        )
        self.save_loc_browse_btn.setText(
            QtWidgets.QApplication.translate("MainWindow", "Browse", None, -1)
        )
        self.start_pt_label.setText(
            QtWidgets.QApplication.translate("MainWindow", "Start Point", None, -1)
        )
        self.stop_pt_label.setText(
            QtWidgets.QApplication.translate("MainWindow", "Stop Point", None, -1)
        )
        self.stop_pt_checkbox.setText(
            QtWidgets.QApplication.translate("MainWindow", "Last", None, -1)
        )
        self.tabs.setTabText(
            self.tabs.indexOf(self.acq_tab),
            QtWidgets.QApplication.translate("MainWindow", "Acquisition", None, -1),
        )
        self.measurement_counter_label.setText(
            QtWidgets.QApplication.translate("MainWindow", "0/0", None, -1)
        )
        self.start_btn.setText(
            QtWidgets.QApplication.translate("MainWindow", "Start", None, -1)
        )
        self.stop_btn.setText(
            QtWidgets.QApplication.translate("MainWindow", "Stop", None, -1)
        )


from pyqtgraph import PlotWidget
