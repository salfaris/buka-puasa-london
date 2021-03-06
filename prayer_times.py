from datetime import datetime
import pandas as pd
import requests
from bs4 import BeautifulSoup

MECCA_URL = 'https://www.muslimpro.com/en/find?country_code=SA&country_name=Saudi%20Arabia&city_name=Mecca&coordinates=21.3890824,39.8579118'
LONDON_URL = 'https://www.muslimpro.com/en/find?coordinates=51.5073509%2C-0.1277583&country_code=GB&country_name=United+Kingdom&city_name=London&date=&convention=precalc'
BRIGHTON_URL = 'https://www.muslimpro.com/Prayer-times-Brighton-United-Kingdom-2654710'
BRIGHTON_MWL_URL = 'https://www.muslimpro.com/Prayer-times-Brighton-United-Kingdom-2654710?date=&convention=MWL&asrjuristic=Standard&highlat=Angle'
CANTERBURY_URL = 'https://www.muslimpro.com/Prayer-times-Canterbury-United-Kingdom-2653877'
MANCHESTER_URL = 'https://www.muslimpro.com/en/Prayer-times-Manchester-United-Kingdom-2643123'

def get_break_fast_time(target_url, limit_today=False):
    mecca_df = get_prayer_time(MECCA_URL, limit_today=limit_today)
    target_df = get_prayer_time(target_url, limit_today=limit_today)

    mecca_fasting_diff = (mecca_df.maghrib.apply(pd.Timestamp) 
                          - mecca_df.subuh.apply(pd.Timestamp))

    early_break_fast_time = (target_df.subuh.apply(pd.Timestamp)
                             + mecca_fasting_diff)
    early_break_fast_time = [datetime.strftime(time, '%H:%M')
                             for time in early_break_fast_time]
    
    target_df['break (early)'] = early_break_fast_time
    return target_df

def get_manch_break_fast_time(limit_today=False):
    return get_break_fast_time(MANCHESTER_URL, limit_today=limit_today)

def get_brighton_break_fast_time(limit_today=False):
    return get_break_fast_time(BRIGHTON_URL, limit_today=limit_today)

def get_london_break_fast_time(limit_today=False):
    return get_break_fast_time(LONDON_URL, limit_today=limit_today)

def get_canterbury_break_fast_time(limit_today=False):
    return get_break_fast_time(CANTERBURY_URL, limit_today=limit_today)

def get_prayer_time(url, limit_today=False):
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'lxml')
    
    table = soup.find('table', {'class': 'prayer-times'})
    table_content = table.find_all('tr')
    table_content = table_content[1:]
    
    dates = []
    subuhs = []
    maghribs = []

    today = datetime.today().day - 1

    for idx, row in enumerate(table_content):
        
        if limit_today:
            # Continue if index is before today's index
            # (calculated based on date).
            if idx < today:
                continue

        row_content = row.find_all('td')

        # Get date of the day
        date = process_text_data(row_content, 0)
        # date = date + ' 2021'
        # date = datetime.strptime(date, '%a %d %b %Y')
        dates.append(date)
        
        # Subuh prayer time
        subuh = process_text_data(row_content, 1)
        subuhs.append(subuh)
        
        # Maghrib prayer time
        maghrib = process_text_data(row_content, 5)
        maghribs.append(maghrib)
        
    df = pd.DataFrame(dict(date=dates, subuh=subuhs, maghrib=maghribs))
    return df

def process_text_data(content, col_idx):
    res = content[col_idx].find(text=True)
    res = str(res)
    return res