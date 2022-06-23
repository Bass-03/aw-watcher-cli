from time import sleep,strftime,gmtime
from datetime import datetime, timedelta, timezone
from dateutil import relativedelta, parser,tz

from aw_core.models import Event
from aw_client.client import ActivityWatchClient

def heartbeat(bucket_name,start_time,activity):
    client = ActivityWatchClient("aw-watcher-cli", testing=False)
    bucket_id = "{}_{}".format(bucket_name, client.client_hostname)
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
    bucket_id = "{}_{}".format(bucket_name, client.client_hostname)
    event_type = "cli_activity"
    client.create_bucket(bucket_id, event_type=event_type)
    shutdown_data = {"label": activity}
    shutdown_event = Event(timestamp=start_time, data=shutdown_data, duration=(end_time -start_time))
    inserted_event = client.insert_event(bucket_id, shutdown_event)
    rd = relativedelta.relativedelta (end_time, start_time)
    print("Spent {:02}:{:02}:{:02} doing {}:".format(rd.hours, rd.minutes, rd.seconds,activity))

# report activity on bucket between 2 dates
# defailts to today
def bucket_report(bucket_name,start_date,end_date):
    client = ActivityWatchClient("aw-watcher-cli", testing=False)
    bucket_id = "{}_{}".format(bucket_name, client.client_hostname)
    query = "RETURN = query_bucket('{}');".format(bucket_id)
    events = client.query(query,start_date,end_date)[0]
    if len(events) == 0:
        print("No events")
        exit()
    events.reverse() #oder from oldest to newest
    # first date
    date = parser.parse(events[0]["timestamp"],default=datetime.now()) - timedelta(hours=6) #- CST
    print(date.date()) #print first date
    day_duration = 0
    total_duration = 0
    cnt = 1
    for event in events:
        total_duration += event["duration"]
        timestamp = parser.parse(event["timestamp"],default=datetime.now()) - timedelta(hours=6) #- CST
        if date.date() != timestamp.date():
            date = timestamp
            print("sum:\t{}".format(format_duration(day_duration))) #duration from prev block
            print("")
            day_duration = event["duration"] #reset duration
            print(date.date()) #print next date
        else:
            day_duration += event["duration"]
        print("{}.\t{}\t{}".format(cnt,format_duration(event["duration"]),event["data"]["label"]))
        cnt += 1
        #print last day_duration when last event is reached
        if event == events[-1]:
            print("sum:\t{}".format(format_duration(day_duration)))
            #Print total report duration
            print("total:\t{}".format(format_duration(total_duration)))

def format_duration(seconds):
    return strftime("%H:%M:%S", gmtime(seconds))
