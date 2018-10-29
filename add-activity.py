import argparse
import aw_watch_cli_help as aw_help
from time import sleep
from datetime import datetime, timedelta, timezone
from dateutil import parser,tz

arg_parser = argparse.ArgumentParser(description='Track activity on a given bucker in ActivityWatch')
arg_parser.add_argument('bucket', metavar='Bucket', type=str, help='Bucket where to track the activity')
arg_parser.add_argument('-a','--activity', dest='activity',help='Activity descritpion')
arg_parser.add_argument('-s','--start_time', dest='start',help='Set a start time', default=datetime.now(timezone.utc))
arg_parser.add_argument('-e','--end_time', dest='end',help='Set an end time, used for setting arbritary activities')

args = arg_parser.parse_args()
#parse start_time if not using the default
if isinstance(args.start, str):
    args.start = parser.parse(args.start,default=datetime.now(timezone(timedelta(hours=-6))))
# If end_time set, just add the event
if args.end:
    #parse end_time if not using the default
    if isinstance(args.end, str):
        args.end = parser.parse(args.end,default=datetime.now(timezone(timedelta(hours=-6))))
    aw_help.shutdown(args.bucket,args.start,args.end,args.activity)
    exit()

# if args.end was not set
try:
    aw_help.heartbeat(args.bucket,args.start,args.activity)
except (KeyboardInterrupt, SystemExit):
    print("   Finishing Activity ........................")
    # Give the dispatcher thread some time to complete sending the last events.
    # If we don't do this the events might possibly queue up and be sent the
    # next time the client starts instead.
    sleep(1)
    end_time = datetime.now(timezone.utc)
    aw_help.shutdown(args.bucket,args.start,end_time,args.activity)
