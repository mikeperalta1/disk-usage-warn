
# Mike's Disk Usage Warn Thing

This is a simple script that will emit a warning to stderr when your disk usage surpasses a configured threshold.
Makes it easy to get emails fron crontab when your disk gets too full

## Requirements

* pyenv

  * pipenv inside

* *logger* program, which should be on most distributions

## Installation

1. Install [pyenv](https://github.com/pyenv/pyenv)

2. cd to this repo's directory and run `$ pyenv install` to get the correct version of python

3. Install pipenv with `$ pip install --upgrade pip pipenv`

4. Initialize the pip environment with `$ pipenv install`

5. Create a yaml configuration file somewhere.

6. Create a crontab entry that will call this script with an argument "--config" followed by the path to your configuration file.

## Command Line Arguments

This script needs command line arguments to work. Primarily, it needs to know the location of at least one valid configuration file

### --config < path >

Specifies a path to a configuration file or directory. If a directory is specified, it will be scanned for configuration files.

### Example Call With Arguments

```shell
cd /path/to/this/repo && pipenv run python main.py --config "/my/config/path-1" --config "/my/config/path-2"
```

## Example Crontab Entry

As mentioned, the easiest way to use this script is with crontabs.
By default, cron jobs will send you an email any time a script outputs to stdout or stderr.
Since this script will output lots of information to stdout,
 and only output to stderr when a disk has become full,
 it's useful to redirect stdout to /dev/null, like so:

```shell
cd /path/to/this/repo && pipenv run python main.py --config "/path/to/config" > /dev/null
```

So, in order to run this script every 5 minutes, use something like the following:

```shell
*/5 * * * * cd /path/to/this/repo && pipenv run python main.py --config "/path/to/config" > /dev/null
```


