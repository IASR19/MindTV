import psycopg2
from pyOpenBCI import OpenBCICyton

def save_eeg_data(participant_id, eeg_data):
    conn = psycopg2.connect(dbname='mindtvdata', user='postgres', password='yourpassword', host='localhost')
    cursor = conn.cursor()
    
    for timestamp, channels in eeg_data:
        cursor.execute("INSERT INTO eeg_data (participant_id, timestamp, channel1, channel2) VALUES (%s, %s, %s, %s)",
                       (participant_id, timestamp, channels[0], channels[1]))
    
    conn.commit()
    cursor.close()
    conn.close()

def eeg_callback(sample):
    timestamp = sample.id  # or any method to get current timestamp
    channels = sample.channels_data
    save_eeg_data(participant_id, [(timestamp, channels)])

board = OpenBCICyton(port='/dev/ttyUSB0', daisy=True)
participant_id = 1  # ID do participante
board.start_stream(eeg_callback)
