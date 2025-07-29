import time

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger
from Data_Collection import Data_Collection_Script
from Data_Collection import jobbankProvince_fetcher
from Data_Storage import Data_Loading_Script
from Data_Quality import Data_Cleaning_Script
from Data_Quality import Load_Cleaned_Data


# pip install apscheduler

def setup_scheduler():
    scheduler = BackgroundScheduler()

    # # Execute every 5 seconds
    # IntervalTrigger(seconds=5)

    # FIXME Adjust the cron expressions as needed.
    tasks = [
        # Execute every day 12:00:00
        (Data_Collection_Script.run, CronTrigger(hour=12, minute=5, second=0)),
        # Execute every hour HH:10:00
        (jobbankProvince_fetcher.main, CronTrigger(minute=10, second=0)),
        # Execute every hour HH:20:00
        (Data_Loading_Script.main, CronTrigger(hour=12, minute=20, second=0)),
        # Execute every hour HH:30:00
        (Data_Cleaning_Script.main, CronTrigger(hour=12, minute=30, second=0)),
        # Execute every hour HH:40:00
        (Load_Cleaned_Data.main, CronTrigger(hour=12, minute=40, second=0)),
    ]
    for task in tasks:
        job = task[0]
        trigger = task[1]
        scheduler.add_job(job, trigger)

    scheduler.start()
    return scheduler


if __name__ == '__main__':
    print("Scheduler starting... Press Ctrl+C to stop.")
    scheduler = setup_scheduler()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Shutting down scheduler...")
        scheduler.shutdown()
