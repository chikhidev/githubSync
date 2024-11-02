import schedule
import time
import subprocess
import datetime

def git_sync():
    print(f"Running sync at {datetime.datetime.now()}")

def run_scheduler(interval='daily'):
    # Configure the schedule based on interval
    if interval == 'each_minute':
        schedule.every().minute.do(git_sync)
    elif interval == 'each_30_minutes':
        schedule.every(30).minutes.do(git_sync)
    elif interval == 'each_hour':
        schedule.every().hour.do(git_sync)
    elif interval == 'daily':
        schedule.every().day.at("00:00").do(git_sync)
    elif interval == 'weekly':
        schedule.every().week.do(git_sync)
    elif interval == 'monthly':
        schedule.every().month.do(git_sync)
    
    print(f"Scheduler started with {interval} interval")
    
    # Keep the script running
    while True:
        schedule.run_pending()
        time.sleep(1)

# Example usage
if __name__ == "__main__":
    run_scheduler('each_minute')