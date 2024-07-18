import sys
import os
import serial.tools.list_ports
import psycopg2
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QComboBox, QTextEdit
from pyOpenBCI import OpenBCICyton
from subprocess import Popen, PIPE

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.serial_port = None
        self.participant_id = 1

    def initUI(self):
        layout = QVBoxLayout()

        # Porta Serial
        self.port_label = QLabel("Selecione a Porta Serial:")
        layout.addWidget(self.port_label)

        self.port_combo = QComboBox(self)
        ports = serial.tools.list_ports.comports()
        for port in ports:
            self.port_combo.addItem(port.device)
        layout.addWidget(self.port_combo)

        # Botões
        self.collect_button = QPushButton('Iniciar Coleta', self)
        self.collect_button.clicked.connect(self.collect_data)
        layout.addWidget(self.collect_button)

        self.preprocess_button = QPushButton('Pré-processar Dados', self)
        self.preprocess_button.clicked.connect(self.preprocess_data)
        layout.addWidget(self.preprocess_button)

        self.train_button = QPushButton('Treinar Modelo', self)
        self.train_button.clicked.connect(self.train_model)
        layout.addWidget(self.train_button)

        self.predict_button = QPushButton('Prever Programa de TV', self)
        self.predict_button.clicked.connect(self.predict_tv_show)
        layout.addWidget(self.predict_button)

        self.output = QTextEdit(self)
        layout.addWidget(self.output)

        self.setLayout(layout)
        self.setWindowTitle('Interface de Coleta e Previsão')
        self.show()

    def get_selected_port(self):
        return self.port_combo.currentText()

    def collect_data(self):
        port = self.get_selected_port()
        self.output.append(f"Iniciando coleta de dados na porta {port}...")

        # Executar scripts de coleta
        eeg_process = Popen([sys.executable, 'collect_eeg_data.py', port], stdout=PIPE, stderr=PIPE)
        gsr_process = Popen([sys.executable, 'collect_gsr_hr_data.py', port], stdout=PIPE, stderr=PIPE)
        
        stdout_eeg, stderr_eeg = eeg_process.communicate()
        stdout_gsr, stderr_gsr = gsr_process.communicate()
        
        self.output.append(stdout_eeg.decode())
        self.output.append(stderr_eeg.decode())
        self.output.append(stdout_gsr.decode())
        self.output.append(stderr_gsr.decode())

        self.output.append("Coleta de dados concluída!")

    def preprocess_data(self):
        self.output.append("Pré-processando dados...")
        process = Popen([sys.executable, 'preprocess_data.py'], stdout=PIPE, stderr=PIPE)
        stdout, stderr = process.communicate()
        self.output.append(stdout.decode())
        self.output.append(stderr.decode())
        self.output.append("Pré-processamento concluído!")

    def train_model(self):
        self.output.append("Treinando modelo...")
        process = Popen([sys.executable, 'train_model.py'], stdout=PIPE, stderr=PIPE)
        stdout, stderr = process.communicate()
        self.output.append(stdout.decode())
        self.output.append(stderr.decode())
        self.output.append("Treinamento do modelo concluído!")

    def predict_tv_show(self):
        self.output.append("Prevendo programa de TV...")
        # Aqui você pode adicionar o código para carregar o modelo treinado e fazer previsões
        self.output.append("Previsão concluída!")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())
