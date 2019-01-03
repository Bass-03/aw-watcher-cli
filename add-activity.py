import argparse
import aw_watch_cli_help as aw_help
import os
from time import sleep
from datetime import datetime, timedelta, timezone
from dateutil import parser,tz

arg_parser = argparse.ArgumentParser(description='Track activity on a given bucket in ActivityWatch')
arg_parser.add_argument('bucket', metavar='Bucket', type=str, help='Bucket where to track the activity')
arg_parser.add_argument('-a','--activity', dest='activity',help='Activity description')
arg_parser.add_argument('-s','--start_time', dest='start',help='Set a start time')
arg_parser.add_argument('-e','--end_time', dest='end',help='Set an end time, used for setting arbitrary activities')
arg_parser.add_argument('-p','--pomodoro',help='start/stop gnome-pomodoro',action='store_true')
arg_parser.add_argument('-r','--report',help='Show activity report',action='store_true')

args = arg_parser.parse_args()

# parse time differently if report was requested
if args.report:
    #start time defaukts to
    if not args.start:
        args.start = datetime.now(timezone(timedelta(hours=-6)))
        args.start = args.start.replace(hour=0, minute=0, second=0, microsecond=0)
    else:
        default_timedate = datetime.now(timezone(timedelta(hours=-6)))
        default_timedate = default_timedate.replace(hour=0, minute=0, second=0, microsecond=0)
        args.start = parser.parse(args.start,default=default_timedate)
    # if end time not set, use now.
    if not args.end:
        args.end = datetime.now(timezone(timedelta(hours=-6)))
    aw_help.bucket_report(args.bucket,args.start,args.end)
    exit()

# If sart_time set,
if args.start:
    # parse the string
    args.start = parser.parse(args.start,default=datetime.now(timezone(timedelta(hours=-6))))
else:
    # default start time
    args.start = datetime.now(timezone(timedelta(hours=-6)))

# If end_time set, just add the event
if args.end:
    #parse end_time if not using the default
    args.end = parser.parse(args.end,default=datetime.now(timezone(timedelta(hours=-6))))
    aw_help.shutdown(args.bucket,args.start,args.end,args.activity)
    exit()

#stat pomodoro timer
if args.pomodoro:
    cmd = 'gnome-pomodoro --start --no-default-window'
    os.system(cmd)
# if args.end was not set
try:
    aw_help.heartbeat(args.bucket,args.start,args.activity)

except (KeyboardInterrupt, SystemExit):
    print("   Finishing Activity ........................")
    # Stop pomodoro
    if args.pomodoro:
        cmd = 'gnome-pomodoro --stop --no-default-window'
        os.system(cmd)
    # Give the dispatcher thread some time to complete sending the last events.
    # If we don't do this the events might possibly queue up and be sent the
    # next time the client starts instead.
    sleep(1)
    end_time = datetime.now(timezone.utc)
    aw_help.shutdown(args.bucket,args.start,end_time,args.activity)
