import schedule
import time
import subprocess
import datetime
import sys

def git_sync():
    print(f"Running sync at {datetime.datetime.now()}")

def run_scheduler(interval='daily'):

    duration = 60

    print(f"Scheduler started with {interval} interval")
    estimated_date = -1
    now = datetime.datetime.now()

    try:
        if int(interval) < 60:
            duration = int(interval)
            schedule.every(int(interval)).minutes.do(git_sync)
            estimated_date = datetime.datetime.now() + datetime.timedelta(minutes=duration)
            print(f"Next run will be at {estimated_date}")
    except:
        pass
    if interval == 'daily':
        schedule.every().day.at("00:00").do(git_sync)
        estimated_date = datetime.datetime(now.year, now.month, now.day, 0, 0, 0) + datetime.timedelta(days=1)
        print(f"Next run will be at {estimated_date}")
    elif interval == 'weekly':
        schedule.every().week.at("00:00").do(git_sync)
        estimated_date = datetime.datetime(now.year, now.month, now.day, 0, 0, 0) + datetime.timedelta(weeks=1)
    elif interval == 'monthly':
        schedule.every().month.at("00:00").do(git_sync)
        estimated_date = datetime.datetime(now.year, now.month, now.day, 0, 0, 0) + datetime.timedelta(months=1)

    print(f"Scheduler will run for {duration} minutes")

    # Keep the script running
    while True:
        schedule.run_pending()
        time.sleep(1)

# Example usage
if __name__ == "__main__":

    if len(sys.argv) > 1:
        run_scheduler(sys.argv[1])
        exit(0)
    print("Please provide an interval")