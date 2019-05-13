# Check-New-Credit-VAMK
Get grades from VAMK's system (WinhaWille) automatically using Selenium and report any new entry. Made for auto run in my Raspberry Pi 3B.

### System requirements
Module | Version
--- | ---
python | 3.5.3
pip | 9.0.1
selenium | 3.141.0
firefox-esr | 52.9.0esr-1
geckodriver | 0.17.0

### System setups
```console
[pi@raspberrypi:~]$ sudo apt-get install python3-pip
[pi@raspberrypi:~]$ sudo apt-get install firefox-esr
[pi@raspberrypi:~]$ sudo apt-get install xvfb
[pi@raspberrypi:~]$ pip3 install pyvirtualdisplay selenium
```
After those installations, note down your firefox and selenium versions. Depending on the versions, you might want to choose a different version of geckodriver. See [Geckodriver supported platforms](https://firefox-source-docs.mozilla.org/testing/geckodriver/geckodriver/Support.html)  
```console
[pi@raspberrypi:~]$ wget https://github.com/mozilla/geckodriver/releases/download/v0.17.0/geckodriver-v0.17.0-arm7hf.tar.gz
[pi@raspberrypi:~]$ sudo tar -xzvf geckodriver-v0.17.0-arm7hf.tar.gz
[pi@raspberrypi:~]$ sudo cp geckodriver /usr/local/bin/
```

### Other requirements
This program needs your VAMK ID (obviously) in the file `IdVamk.txt` and Gmail ID in `IdGmailApp.txt` for reporting.  
The Gmail username is your own email address. For the password, it is recommended to use [Gmail app password](https://support.google.com/accounts/answer/185833?hl=en) to avoid saving your main account password in plain text and pass 2-Step-Verification.  

### Autorun setup
In my device, I use [Cron](https://www.raspberrypi.org/documentation/linux/usage/cron.md) to automate tasks.  
```console
[pi@raspberrypi:~]$ sudo crontab -e
```
Since VAMK's system normally updates some hours before midnight, I add the line below at the end of the file to run the program at midnight everyday.  
```
0 0 * * * cd /home/pi/python/check-new-credit && python3 ./check-new-credit.py &>/dev/null
```
