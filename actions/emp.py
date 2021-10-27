import threading
import requests
import json
import time
import string
import random
# Function Scheduler 
def scheduler(interval, times = -1):
    def outer_wrap(function):
        def wrap(*args, **kwargs):
            reminder = threading.Event()
            def inner_wrap():
                i = 0
                while i != times and not reminder.isSet():
                    reminder.wait(interval)
                    function(*args, **kwargs)
                    i += 1
            threads = threading.Timer(0, inner_wrap)
            threads.daemon = False
            threads.start()
            return reminder
        return wrap
    return outer_wrap

@scheduler(10)
def invoke_workday_api():
    data = {"name": "EXTERNAL_dry_plant", "entities": {"plant":"orchid"}}
    json_data = json.dumps(data)
    res = ''.join(random.choices(string.ascii_uppercase +
                             string.digits, k = 32))
    #cid = "53fa061d01c6407390271efeb029cd21"
    #url = "http://localhost:5005/conversations/a:1nPGWfB4OnyNXl2o3tMGNNIlYE1e2hzavXtpWyPVzKZB59N7TYyCU-N-xnGKepSzP_fRdVyhtJ8a9z3Jy7CkCMdE9q20HwkpMGr3r77pPTrPkGi5li7eAYBxR_07rDNeg/trigger_bot_intent?output_channel=latest"
    url = f"http://localhost:5005/conversations/{res}/trigger_intent?output_channel=latest"
    response = requests.post(url, data=json_data)

if __name__ == "__main__":
    s_obj = invoke_workday_api()
    time.sleep(10)
    s_obj.set()