from crontab import CronTab
import os

cron = CronTab(user='sua')

job1 = cron.new(command=f"cd {os.getcwd()} && python3.6 publish_tp_course.py -> cron_out.log")

job1.minute.every(1)

for item in cron:
    print(item)

cron.write()
