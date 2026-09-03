import sys
import socketio
import qdarktheme
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QScrollArea, QLabel, QHBoxLayout
from PyQt5.QtCore import QThread, pyqtSignal, Qt, QTimer
from PyQt5.QtGui import QFont, QColor
import pyqtgraph as pg
import time
import numpy as np

class SocketIOClient(QThread):
    waves_received = pyqtSignal(dict)
    locmag_received = pyqtSignal(dict)

    def __init__(self):
        super().__init__()
        self.sio = socketio.Client()

        @self.sio.event
        def connect():
            print('Connection established with EEWS Backend')

        @self.sio.event
        def disconnect():
            print('Disconnected from server')

        @self.sio.on('waves-data')
        def on_waves(data):
            self.waves_received.emit(data)
            
        @self.sio.on('loc-mag-data')
        def on_locmag(data):
            self.locmag_received.emit(data)

    def run(self):
        try:
            self.sio.connect('http://localhost:3333')
            self.sio.wait()
        except Exception as e:
            print(f"Socket connection error: {e}")

class EEWSDashboard(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("EEWS Command Center")
        self.resize(1200, 800)
        self.data_store = {}
        self.plot_widgets = {}

        # Apply dark theme
        qdarktheme.setup_theme("dark")

        # Main Layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)
        
        # Header Status
        self.header_label = QLabel("🟢 STATUS: AMAN - MENDENGARKAN SINYAL SEISMIK")
        self.header_label.setAlignment(Qt.AlignCenter)
        self.header_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #10b981; padding: 10px; border-radius: 5px; background: rgba(16, 185, 129, 0.1); border: 1px solid #10b981;")
        self.layout.addWidget(self.header_label)

        # Scroll Area for Plots
        self.scroll_area = QScrollArea(self.central_widget)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet("border: none;")
        self.layout.addWidget(self.scroll_area)
        
        self.scroll_widget = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_widget)
        self.scroll_area.setWidget(self.scroll_widget)

        # Alert Reset Timer
        self.alert_timer = QTimer(self)
        self.alert_timer.timeout.connect(self.reset_alert)

        # Start Socket Client
        self.socket_client = SocketIOClient()
        self.socket_client.waves_received.connect(self.update_waves)
        self.socket_client.locmag_received.connect(self.trigger_alert)
        self.socket_client.start()

    def reset_alert(self):
        self.header_label.setText("🟢 STATUS: AMAN - MENDENGARKAN SINYAL SEISMIK")
        self.header_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #10b981; padding: 10px; border-radius: 5px; background: rgba(16, 185, 129, 0.1); border: 1px solid #10b981;")

    def trigger_alert(self, data):
        station = data.get('station', 'UNKNOWN')
        preds = data.get('predictions_loc_mag', [[0,0,0,0]])[0]
        mag = preds[3]
        depth = preds[2]
        
        if mag > 3.0:
            alert_text = f"🚨 PERINGATAN GEMPA [STASIUN {station}] | MAGNITUDO {mag:.1f} | KEDALAMAN {depth:.1f} KM 🚨"
            self.header_label.setText(alert_text)
            self.header_label.setStyleSheet("font-size: 28px; font-weight: bold; color: #ffffff; padding: 15px; border-radius: 5px; background: #ef4444; border: 2px solid #b91c1c;")
            self.alert_timer.start(10000) # Reset after 10 seconds

    def update_waves(self, data):
        key = f"{data['station']}-{data['channel']}"
        sampling_rate = data['sampling_rate']
        new_y = data['data']
        
        if sampling_rate < 10:
            return

        if key not in self.data_store:
            # Initialize storage
            self.data_store[key] = {
                'y': list(new_y),
                'sampling_rate': sampling_rate
            }
            self.create_plot(key, data['station'], data['channel'], sampling_rate)
        else:
            # Append data and maintain max 60 seconds
            self.data_store[key]['y'].extend(new_y)
            max_samples = int(60 * sampling_rate)
            if len(self.data_store[key]['y']) > max_samples:
                self.data_store[key]['y'] = self.data_store[key]['y'][-max_samples:]
            
            # Update plot
            y_data = self.data_store[key]['y']
            x_data = list(range(-len(y_data), 0))
            self.plot_widgets[key].setData(x=x_data, y=y_data)

    def create_plot(self, key, station, channel, sr):
        plot = pg.PlotWidget()
        plot.setTitle(f"Stasiun {station} - {channel} ({sr}Hz)", color='#38bdf8', size='14pt')
        plot.setLabel('left', 'Amplitude', color='#94a3b8')
        plot.showGrid(x=True, y=True, alpha=0.3)
        plot.setBackground('#0f172a')
        
        y_data = self.data_store[key]['y']
        x_data = list(range(-len(y_data), 0))
        
        plot_data = plot.plot(x=x_data, y=y_data, pen=pg.mkPen(color='#38bdf8', width=2))
        plot.setXRange(-60 * sr, 0)
        
        self.plot_widgets[key] = plot_data
        
        container = QWidget()
        layout = QVBoxLayout()
        container.setLayout(layout)
        layout.addWidget(plot)
        self.scroll_layout.addWidget(container)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = EEWSDashboard()
    window.show()
    sys.exit(app.exec_())
