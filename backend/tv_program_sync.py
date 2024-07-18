import requests
import datetime

API_KEY = 'LoQ_ikAEGdJy9G0LDlXnwYnyROXq2h2w'
TV_API_URL = 'https://api.tvmaze.com/schedule?country=US'

def fetch_tv_schedule():
    response = requests.get(TV_API_URL)
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
            return show
    return None

def main():
    tv_schedule = fetch_tv_schedule()
    current_show = get_current_show(tv_schedule)
    if current_show:
        print(f"Current show: {current_show['show']['name']}")
    else:
        print("No show currently airing.")

if __name__ == '__main__':
    main()
