import numpy as np
from scipy.signal import butter, lfilter
import psycopg2

def butter_bandpass(lowcut, highcut, fs, order=5):
    nyquist = 0.5 * fs
    low = lowcut / nyquist
    high = highcut / nyquist
    b, a = butter(order, [low, high], btype='band')
    return b, a

def bandpass_filter(data, lowcut, highcut, fs, order=5):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = lfilter(b, a, data)
    return y

# Carregar dados do banco de dados
def load_data():
    conn = psycopg2.connect(dbname='neurodata', user='postgres', password='yourpassword', host='localhost')
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM eeg_data WHERE participant_id = %s", (1,))
    eeg_data = cursor.fetchall()
    
    cursor.execute("SELECT * FROM gsr_hr_data WHERE participant_id = %s", (1,))
    gsr_data = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return eeg_data, gsr_data

eeg_data, gsr_data = load_data()

# Pré-processar dados EEG
fs = 250  # Frequência de amostragem
lowcut = 1.0
highcut = 50.0
eeg_channels = [data[3:] for data in eeg_data]  # Ajuste conforme a estrutura dos dados
eeg_filtered = [bandpass_filter(channel, lowcut, highcut, fs) for channel in np.array(eeg_channels).T]

# Organizar os dados de acordo com o programa de TV atual
eeg_data_processed = [(data[0], data[1], data[2], *channels) for data, channels in zip(eeg_data, np.array(eeg_filtered).T)]
gsr_data_processed = [(data[0], data[1], data[2], data[3], data[4], data[5], data[6]) for data in gsr_data]

# Salvar os dados pré-processados em arquivos para treinamento
np.savetxt('eeg_data_processed.csv', eeg_data_processed, delimiter=',', fmt='%s')
np.savetxt('gsr_data_processed.csv', gsr_data_processed, delimiter=',', fmt='%s')
