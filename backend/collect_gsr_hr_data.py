import serial
import psycopg2
import time

def save_gsr_hr_data(participant_id, ir_value, bpm, avg_bpm, gsr_value):
    conn = psycopg2.connect(dbname='mindtvdata', user='postgres', password='yourpassword', host='localhost')
    cursor = conn.cursor()
    
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute("INSERT INTO gsr_hr_data (participant_id, timestamp, ir_value, bpm, avg_bpm, gsr_value) VALUES (%s, %s, %s, %s, %s, %s)",
                   (participant_id, timestamp, ir_value, bpm, avg_bpm, gsr_value))
    
    conn.commit()
    cursor.close()
    conn.close()

ser = serial.Serial('/dev/tty.usbmodem14101', 115200)  # Ajuste a porta conforme necessário
participant_id = 1  # ID do participante

while True:
    if ser.in_waiting:
        line = ser.readline().decode('utf-8').strip()
        ir_value, bpm, avg_bpm, gsr_value = map(int, line.split(','))
        save_gsr_hr_data(participant_id, ir_value, bpm, avg_bpm, gsr_value)
