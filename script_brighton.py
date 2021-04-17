from sys import argv, exit
from prayer_times import get_brighton_break_fast_time

if __name__ == '__main__':
    
    limit_today=True
    
    if len(argv) > 1:    
        if ('-f' in argv) or ('--full' in argv):
            limit_today=False
        else:
            print("Unknown argument used. For full display, use '-f' or '--full'.")
            exit(1)
    
    print("Getting Brighton buka puasa time...")
    df = get_brighton_break_fast_time(limit_today=limit_today)
    print(df)
    