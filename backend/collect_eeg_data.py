import psycopg2
from pyOpenBCI import OpenBCICyton
import requests
import datetime
import time

def save_eeg_data(participant_id, eeg_data, current_show):
    conn = psycopg2.connect(dbname='neurodata', user='postgres', password='yourpassword', host='localhost')
    cursor = conn.cursor()
    
    for timestamp, channels in eeg_data:
        cursor.execute("INSERT INTO eeg_data (participant_id, timestamp, channel1, channel2, current_show) VALUES (%s, %s, %s, %s, %s)",
                       (participant_id, timestamp, channels[0], channels[1], current_show))
    
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

def eeg_callback(sample):
    tv_schedule = fetch_tv_schedule()
    current_show = get_current_show(tv_schedule)
    
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    channels = sample.channels_data
    save_eeg_data(participant_id, [(timestamp, channels)], current_show)

board = OpenBCICyton(port='/dev/tty.usbserial-1420', daisy=True)
participant_id = 1  # ID do participante
board.start_stream(eeg_callback)
