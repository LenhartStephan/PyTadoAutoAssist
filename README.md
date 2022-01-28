# PyTadoAutoAssist
## About the script
The PyTadoAutoAssist-Script automates the open-window and the home-and-away-detection and activation for Tado. It runs every 10s and only uses the information available in the (unofficial) [Tado API](https://github.com/wmalgadey/PyTado).
### Open window detection
The Script checks in all rooms, if an open window has been detected and if so, it activates the open window mode in that room. 
### Home and away detection
For home and away, it checks the status of all of your Tado client devices and if no one is home, it activates the away mode, if at least one person is detected at home, it activates the home mode. You need to have at least one device running the tado app with geofencing enabled.

## Dependencies
The Auto Assist Script is dependent on [PyTado](https://github.com/wmalgadey/PyTado). Install it with `pip install python-tado`.

## Usage 
Fill in your login-information into the loginlist variable. Multiple accounts (and thus homes) are supported:\
`loginlist = [('user1@example.com', 'PASSWORD1'), ('user2@example.com', 'PASSWORD2')]`\
\
If needed edit the name of the logfile:\
`log = "tado-autoassist.log"`
You can also specify how many log entries are saved (default is 10):
```
def writeToLog(msg):
    filelength = 10
```
\
Then just run the script `python3 autoassist.py`. As long as its running, home-and-away and the open-window-detection are automated.
