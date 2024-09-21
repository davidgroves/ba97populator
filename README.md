# NO LONGER WORKS.

This no longer works as BA have made changes to the website and this screenscraping doesn't work anymore.


# Purpose

A program to take British Airways flight bookings from the 
[British Airways website](https://www.britishairways.com)
and prepare well formatted submissions for the flight tracking site [BA97](https://ba97.com/).

# How to use

You need Python 3.7, to install the packages in requirements.txt (ideally in a Python venv),
and to have Firefox and the [Gecko Selenium driver](https://github.com/mozilla/geckodriver/releases)
installed.

Rename example-credentials.json to credentials.json and fill it in. 

Then you just run the program and it should write your flights to STDOUT.

# Bugs

- I've only tested this on my own machine (a Windows 10 PC in this case).
- It may not cope with some more complex itineraries, please report this if you care.
- It might not cope with plane types I've not seen or cabin class names I've not thought of. 
This should be easy to fix.
- It can be a bit slow. BA have plenty of wierd places where you need to just wait, 
regardless of if the browser thinks it is ready or not, so there are lots of long sleeps.

# Example Output

    01Mar2019 1935 BA2966 LGW GLA Y A319 10A
    03Mar2019 2110 BA2965 GLA LGW Y A319 10A
    04Mar2019 0825 BA0117 LHR JFK F B747 01A
    04Mar2019 1630 BA2466 JFK SFO F A321 01A
    10Mar2019 1115 BA4388 SFO JFK J A321 09A
    11Mar2019 0015 BA0182 JFK LHR J B777 10K

# Contact

- Feedback, bug reports, ranting to ba97populator (at sign) fibrecat.org.
