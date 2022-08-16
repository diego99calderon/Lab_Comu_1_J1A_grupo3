#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Transmisor Am
# Author: J1A Grupo2
# Copyright: UIS
# GNU Radio version: 3.9.5.0

from distutils.version import StrictVersion

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print("Warning: failed to XInitThreads()")

import os
import sys
sys.path.append(os.environ.get('GRC_HIER_PATH', os.path.expanduser('~/.grc_gnuradio')))

from EnvolventeComplejaDSBSC import EnvolventeComplejaDSBSC  # grc-generated hier_block
from calculoPotencia import calculoPotencia  # grc-generated hier_block
from gnuradio import analog
from gnuradio import gr
from gnuradio.filter import firdes
from gnuradio.fft import window
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import uhd
import time
from gnuradio.qtgui import Range, RangeWidget
from PyQt5 import QtCore



from gnuradio import qtgui

class TransmisorAm(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Transmisor Am", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Transmisor Am")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "TransmisorAm")

        try:
            if StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
                self.restoreGeometry(self.settings.value("geometry").toByteArray())
            else:
                self.restoreGeometry(self.settings.value("geometry"))
        except:
            pass

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 200e3
        self.fc = fc = 50e6
        self.Ka = Ka = 1
        self.GTX = GTX = 0
        self.Ac = Ac = 100e-3
        self.A = A = 1

        ##################################################
        # Blocks
        ##################################################
        self._fc_range = Range(50e6, 2.2e9, 1e6, 50e6, 200)
        self._fc_win = RangeWidget(self._fc_range, self.set_fc, "Frecuencia Portadora", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._fc_win)
        self._Ka_range = Range(0, 4, 100e-6, 1, 200)
        self._Ka_win = RangeWidget(self._Ka_range, self.set_Ka, "Coeficiente Ka", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._Ka_win)
        self._GTX_range = Range(0, 30, 1, 0, 200)
        self._GTX_win = RangeWidget(self._GTX_range, self.set_GTX, "Ganancia del TX", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._GTX_win)
        self._Ac_range = Range(0, 1, 100e-6, 100e-3, 200)
        self._Ac_win = RangeWidget(self._Ac_range, self.set_Ac, "Amplitud portadora", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._Ac_win)
        self._A_range = Range(0, 1, 100e-6, 1, 200)
        self._A_win = RangeWidget(self._A_range, self.set_A, "Amplitud Modulante", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._A_win)
        self.uhd_usrp_sink_0 = uhd.usrp_sink(
            ",".join(("", '')),
            uhd.stream_args(
                cpu_format="fc32",
                args='',
                channels=list(range(0,1)),
            ),
            "",
        )
        self.uhd_usrp_sink_0.set_samp_rate(samp_rate)
        self.uhd_usrp_sink_0.set_time_now(uhd.time_spec(time.time()), uhd.ALL_MBOARDS)

        self.uhd_usrp_sink_0.set_center_freq(fc, 0)
        self.uhd_usrp_sink_0.set_antenna("TX/RX", 0)
        self.uhd_usrp_sink_0.set_gain(GTX, 0)
        self.calculoPotencia_0 = calculoPotencia(
            l_vect=1024,
        )

        self.top_layout.addWidget(self.calculoPotencia_0)
        self.analog_sig_source_x_0 = analog.sig_source_f(samp_rate, analog.GR_COS_WAVE, 1000, A, 0, 0)
        self.EnvolventeComplejaDSBSC_0 = EnvolventeComplejaDSBSC(
            Ac=Ac,
            k=Ka,
        )


        ##################################################
        # Connections
        ##################################################
        self.connect((self.EnvolventeComplejaDSBSC_0, 0), (self.uhd_usrp_sink_0, 0))
        self.connect((self.analog_sig_source_x_0, 0), (self.EnvolventeComplejaDSBSC_0, 0))
        self.connect((self.analog_sig_source_x_0, 0), (self.calculoPotencia_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "TransmisorAm")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.analog_sig_source_x_0.set_sampling_freq(self.samp_rate)
        self.uhd_usrp_sink_0.set_samp_rate(self.samp_rate)

    def get_fc(self):
        return self.fc

    def set_fc(self, fc):
        self.fc = fc
        self.uhd_usrp_sink_0.set_center_freq(self.fc, 0)

    def get_Ka(self):
        return self.Ka

    def set_Ka(self, Ka):
        self.Ka = Ka
        self.EnvolventeComplejaDSBSC_0.set_k(self.Ka)

    def get_GTX(self):
        return self.GTX

    def set_GTX(self, GTX):
        self.GTX = GTX
        self.uhd_usrp_sink_0.set_gain(self.GTX, 0)

    def get_Ac(self):
        return self.Ac

    def set_Ac(self, Ac):
        self.Ac = Ac
        self.EnvolventeComplejaDSBSC_0.set_Ac(self.Ac)

    def get_A(self):
        return self.A

    def set_A(self, A):
        self.A = A
        self.analog_sig_source_x_0.set_amplitude(self.A)




def main(top_block_cls=TransmisorAm, options=None):

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()

    tb.show()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    qapp.exec_()

if __name__ == '__main__':
    main()
