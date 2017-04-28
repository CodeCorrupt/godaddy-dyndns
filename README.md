# This has been deprecated in favor of a Node based solution
See [godaddy-dyndns](https://github.com/CodeCorrupt/godaddy-dyndns)

# godaddy-dyndns
DynDNS-like public IP auto-updater script for GoDaddy.

The script uses `ipify.org` to figure out the machine's public IP. It only accesses GoDaddy when if the IP has changed since the last (successful) script invocation. It logs all its activities to the file `godaddy-dyndns.log` (and automatically rotates the log).

Based on [Sascha's script with the same name](https://saschpe.wordpress.com/2013/11/12/godaddy-dyndns-for-the-poor/).

## Setup
#### Automatic
*WARNING!* setup.sh has *ZERO* error checking. All this script does is automate the steps in Manual.

Run the setup script:

    ./setup.sh

Edit `godaddy-dyndns.conf` with your account info.
You *must* add at least one domain and record for the script to do anything.

#### Manual
After cloning this repo be sure to initialize the submodule pygodaddy-src

    git submodule init
    git submodule update

Ensure the symbolic link to ./pygodaddy-src/pygodaddy is correct

Setup a Python venv:

    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    deactivate

Copy the file `godaddy-dyndns.conf.template` to `godaddy-dyndns.conf` and add your information to the new file.

    cp godaddy-dyndns.conf.template godaddy-dyndns.conf

And lastly add `godaddy-dyndns.sh` to your crontab file, e.g.:

    */5 * * * * /path/to/script/godaddy-dyndns.sh
    @reboot sleep 30 && /path/to/script/godaddy-dyndns.sh

The above makes sure that the script runs when your machine boots, and then every hour after that. `sleep` is used to increase the chance that the network has started before the script is run.
