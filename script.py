from datetime import datetime

import pandas as pd
import requests
from bs4 import BeautifulSoup

MECCA_URL = 'https://www.muslimpro.com/en/find?country_code=SA&country_name=Saudi%20Arabia&city_name=Mecca&coordinates=21.3890824,39.8579118'
LONDON_URL = 'https://www.muslimpro.com/en/find?country_code=GB&country_name=United%20Kingdom&city_name=London&coordinates=51.5073509,-0.1277583'

def get_london_break_fast_time():
    mecca_df = get_prayer_time(MECCA_URL)
    london_df = get_prayer_time(LONDON_URL)

    mecca_fasting_diff = (mecca_df.maghrib.apply(pd.Timestamp) 
                          - mecca_df.subuh.apply(pd.Timestamp))

    early_break_fast_time = (london_df.subuh.apply(pd.Timestamp) 
                             + mecca_fasting_diff)
    early_break_fast_time = [datetime.strftime(time, '%H:%M') 
                             for time in early_break_fast_time]
    
    london_df['break (early)'] = early_break_fast_time
    return london_df

def get_prayer_time(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'lxml')
    
    table = soup.find('table', {'class': 'prayer-times'})
    table_content = table.find_all('tr')
    table_content = table_content[1:]
    
    dates = []
    subuhs = []
    maghribs = []

    for row in table_content:
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

def process_text_data(content, for_col):
    res = content[for_col].find(text=True)
    res = str(res)
    return res