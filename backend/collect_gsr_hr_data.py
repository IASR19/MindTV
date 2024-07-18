import serial
import psycopg2
import time
import requests
import datetime

def save_gsr_hr_data(participant_id, ir_value, bpm, avg_bpm, gsr_value, current_show):
    conn = psycopg2.connect(dbname='neurodata', user='postgres', password='yourpassword', host='localhost')
    cursor = conn.cursor()
    
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute("INSERT INTO gsr_hr_data (participant_id, timestamp, ir_value, bpm, avg_bpm, gsr_value, current_show) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                   (participant_id, timestamp, ir_value, bpm, avg_bpm, gsr_value, current_show))
    
    conn.commit()
    cursor.close()
    conn.close()

def fetch_tv_schedule():
    response = requests.get('https://api.tvmaze.com/schedule?country=US')
    if response.status_code == 200:
        return response.json()
    else:
        return []

def get_current_show(tv_schedule):
    now = datetime.datetime.now()
    for show in tv_schedule:
        start_time = datetime.datetime.strptime(show['airtime'], '%H:%M')
        duration = datetime.timedelta(minutes=show['runtime'])
        end_time = start_time + duration
        if start_time.time() <= now.time() <= end_time.time():
            return show['show']['name']
    return "No show currently airing"

ser = serial.Serial('/dev/tty.usbserial-1420', 115200)  # Ajuste a porta conforme necessário
participant_id = 1  # ID do participante

while True:
    tv_schedule = fetch_tv_schedule()
    current_show = get_current_show(tv_schedule)
    
    if ser.in_waiting:
        line = ser.readline().decode('utf-8').strip()
        ir_value, bpm, avg_bpm, gsr_value = map(float, line.split(','))
        save_gsr_hr_data(participant_id, ir_value, bpm, avg_bpm, gsr_value, current_show)
