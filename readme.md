# AW Watcher CLI

A CLI to track activities in [activitywatch](https://github.com/ActivityWatch/activitywatch).


## Getting Started



### Installing

Install Activity Watch system wide to get the aw-client library, follow the [docs](https://activitywatch.readthedocs.io/en/latest/getting-started.html#installation)

Place this scrip wherever you want, for instance `~/activitywatch/aw-watcher-cli`

Add Aliases to your `.bashrc` or equivalent, for instance

``` bash
alias work="python3 /home/mundo/activitywatch/aw-watcher-cli/add-activity.py work"
```

Add as many buckets as you want, for instance

``` bash
alias homework="python3 /home/mundo/activitywatch/aw-watcher-cli/add-activity.py homework"
```

``` bash
alias netflix="python3 /home/mundo/activitywatch/aw-watcher-cli/add-activity.py netflix"
```

## Usage

If you did it my way, you already added a bucket in your alias, this way you reduce the change for a typo when logging your activity.

So all you need to do is

``` bash
bucket -a "I am doing this now"
```

This will start a timer on your current terminal window, to end the activity just interrupt it (ctl + C)

You can also ask for help

```
bucket -h
```

```
usage: add-activity.py [-h] [-a ACTIVITY] [-s START] [-e END] Bucket

Track activity on a given bucker in ActivityWatch

positional arguments:
  Bucket                Bucket where to track the activity

optional arguments:
  -h, --help            show this help message and exit
  -a ACTIVITY, --activity ACTIVITY
                        Activity descritpion
  -s START, --start_time START
                        Set a start time
  -e END, --end_time END
                        Set an end time, used for setting arbritary activities


```


## Contributing

Branch it, PR me

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

*   The activity Watch guys
*   Hat tip to anyone whose code was used
*   Inspiration
*   etc
