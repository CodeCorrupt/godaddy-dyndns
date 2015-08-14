# godaddy-dyndns
DynDNS-like public IP auto-updater script for GoDaddy.

The script uses `ipify.org` to figure out the machine's public IP. It only accesses GoDaddy when if the IP has changed since the last (successful) script invocation. It logs all its activities to the file `godaddy-dyndns.log` (and automatically rotates the log).

Based on [Sascha's script with the same name](https://saschpe.wordpress.com/2013/11/12/godaddy-dyndns-for-the-poor/).

## Setup

Copy the file `godaddy-dyndns.conf.template` to `godaddy-dyndns.conf` and add your GoDaddy username and password to the new file.

Then setup a Python venv:

    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    deactivate

And lastly add `godaddy-dyndns.sh` to your crontab file, e.g.:

    0 * * * * /path/to/script/godaddy-dyndns.sh
    @reboot sleep 30 && /path/to/script/godaddy-dyndns.sh

The above makes sure that the script runs when your machine boots, and then every hour after that. `sleep` is used to increase the chance that the network has started before the script is run.

## TODO

Maybe one should add some kind of max number of updates per day? In case the script breaks in some way.
