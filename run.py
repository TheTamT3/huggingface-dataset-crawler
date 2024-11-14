import subprocess
import time

import schedule


def run_schedule():
    subprocess.run(["python", "src/main.py"])


schedule.every(1).minutes.do(run_schedule)
# schedule.every(14).days.do(run_bash_script)

while True:
    schedule.run_pending()
    time.sleep(1)
