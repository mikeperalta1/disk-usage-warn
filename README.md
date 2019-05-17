
# Mike's Disk Usage Warn Thing

This is a simple script that will emit a warning to stderr when your disk usage surpasses a configured threshold. StdErr output was chosen for its simplicity, and because it's very easy to configure a cron job to send you an email any time an error occurs.

## Requirements

* Python3

* Python *pyaml* module
  
  Example:
  
  ```sudo pip3 install pyaml```

* *logger* program, which should be on most distributions

## Installation

1. First, make sure you have python3 and pip3 installed

2. Use pip3 to make sure you have the python module "pyaml" installed

3. Create a configuration file somewhere. 

4. Create a Crontab entry that will call this script with an argument "--config" followed by the path to your configuration file.

(examples found below)

## Command Line Arguments

This script needs command line arguments to work. Primarily, it needs to know the location of at least one valid configuration file

### --config < path >

Specifies a path to a configuration file or directory. If a directory is specified, it will be scanned for configuration files.

### Example Call With Arguments

Assuming you can invoke *Python 3* with the command ```python3```, here's a quick example using two configuration files:

```
python3 /path/to/disk-usage-warn --config "/my/config/path-1" --config "/my/config/path-2"
```

## Example Crontab Entry

As mentioned, the easiest way to use this script is with Crontabs. By default, cron jobs will send you an email any time a script outputs to stdout or stderr. Since this script will output lots of information onto stdout, and only output to stderr when a disk has become full, it's useful to redirect stdout to /dev/null, like so:

```bash
python3 /path/to/disk-usage-warn --config "/path-to-config" > /dev/null
```

So, in order to run this script every 5 minutes, use something like the following:

```bash
*/5 * * * * python3 /path/to/disk-usage-warn --config "/path-to-config" > /dev/null
```

The examples above assume you can invoke *Python 3* with the command ```python3```.



