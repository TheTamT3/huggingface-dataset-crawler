import subprocess
import time

import schedule


def run_bash_script():
    subprocess.run(["bash", "scripts/run_scripts.sh"])


schedule.every(1).minutes.do(run_bash_script)
# schedule.every(14).days.do(run_bash_script)

while True:
    schedule.run_pending()
    time.sleep(1)
