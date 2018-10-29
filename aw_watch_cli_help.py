from time import sleep
from datetime import datetime, timedelta, timezone
from dateutil import relativedelta

from aw_core.models import Event
from aw_client import ActivityWatchClient

def heartbeat(bucket_name,start_time,activity):
    client = ActivityWatchClient("aw-watcher-cli", testing=False)
    bucket_id = "{}_{}".format(bucket_name, client.hostname)
    event_type = "cli_ping"
    client.create_bucket(bucket_id, event_type=event_type)
    # Asynchronous loop
    with client:
        heartbeat_data = {"label": "heartbeat"}
        now = datetime.now(timezone.utc)
        heartbeat_event = Event(timestamp=now, data=heartbeat_data)
        sleeptime = 1
        #Sending hearbeat until keyboard interrup
        second = 1
        while(True):
            # The duration between the heartbeats will be less than pulsetime, so they will get merged.
            rd = relativedelta.relativedelta (now, start_time)
            print("Doing: {} for {:02}:{:02}:{:02}".format(activity,rd.hours, rd.minutes, rd.seconds),end="\r")
            client.heartbeat(bucket_id, heartbeat_event, pulsetime=sleeptime+1, queued=True)
            # Sleep a second until next heartbeat
            sleep(sleeptime)
            # Update timestamp for next heartbeat
            heartbeat_event.timestamp = datetime.now(timezone.utc)
            # update now
            now = heartbeat_event.timestamp
            second += 1


# End and send event
# insert an event
def shutdown(bucket_name,start_time,end_time,activity):
    client = ActivityWatchClient("aw-watcher-cli", testing=False)
    bucket_id = "{}_{}".format(bucket_name, client.hostname)
    event_type = "cli_activity"
    client.create_bucket(bucket_id, event_type=event_type)
    shutdown_data = {"label": activity}
    shutdown_event = Event(timestamp=start_time, data=shutdown_data, duration=(end_time -start_time))
    inserted_event = client.insert_event(bucket_id, shutdown_event)
    rd = relativedelta.relativedelta (end_time, start_time)
    print("Spent {:02}:{:02}:{:02} doing {}:".format(rd.hours, rd.minutes, rd.seconds,activity))
