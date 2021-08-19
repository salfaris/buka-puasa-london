from sys import argv, exit
from datetime import datetime
from prayer_times import get_london_break_fast_time
import pandas as pd

limit_today = True

def break_fast_time_to_df(csv_path):
    df = get_london_break_fast_time()
    df.to_csv(csv_path, index=False)

if __name__ == '__main__':
    
    csv_path = 'early-maghrib-london.csv'
    
    if len(argv) > 1:    
        if ('-f' in argv) or ('--full' in argv):
            limit_today = False
        elif ('--fetch' in argv):
            break_fast_time_to_df(csv_path)
        else:
            print("Unknown argument used. For full display, use '-f' or '--full'.")
            exit(1)
    
    print("Getting London buka puasa time...")
    today = datetime.today().day
    skiprow_ub = today if limit_today else 0
    try:
        df = pd.read_csv(csv_path, skiprows=range(1, skiprow_ub))
    except FileNotFoundError:
        break_fast_time_to_df(csv_path)
        df = pd.read_csv(csv_path, skiprows=range(1, skiprow_ub))
    
    print(df)