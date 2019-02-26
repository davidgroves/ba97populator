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
- It might not cope with plane types I've not seen or selling class names I've not thought of. 
This should be easy to fix.
- It can be a bit slow. BA have plenty of wierd places where you need to just wait, 
regardless of if the browser thinks it is ready or not, so there are lots of long sleeps.

# Contact

- Feedback, bug reports, ranting to ba97populator (at sign) fibrecat.org.