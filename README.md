# Programming Internet of Things

## Branches

- **master:** Mostly Documentation
- **ass1:** Assignment 1 master branch
- **ass1-dev:** Assignment 1 development branch

## Aim

The aim of this assignment is to write a small IoT application using Raspberry Pi and Sense HAT in
Python language.
Some of the tasks of this assignment will require self-exploration and research, you will not find the
answer in lectures notes and/or tutorials.
You must attend a **15-minute** demo session to get assignment 1 marked during week 6
(April 08-12, 2019). A schedule and a booking document will be published soon. You must submit
the assignment prior to demo. **No submission → No demo → No marks.**

## Requirements

You must adhere to the following requirements:

a. Only Raspberry Pi model 3 B/B+ **may be** used.  
b. You **must use** Python 3.5 or > 3.5 to complete the tasks. **Older versions must not be used.**  
c. Whether working individually or in a group, you **must use a version control system** of some sorts such as *GitHub, Bitbucket*, etc...  
d. You **must stick** to the standard style guide for your Python code: [PEP 8](https://www.python.org/dev/peps/pep-0008/)  
e. Your **Python code must be object-oriented.**  

## Tasks

### Task a (10 Marks)

A JSON config file will store a temperature and humidity range. This file should be called `config.json`.

```json
{
    "min_temperature": 20,
    "max_temperature": 30,
    "min_humitidy": 50,
    "max_humitidy":60,
}
```

Create a python file called `monitorAndNotify.py` which will log the current time, temp, and humidity to a database every minute (you can choose what type of db to use: SQLite 3.x or MySQL)

> In this course we cover SQLite & MySQL, if you want to use another database, please feel free to do so. Use of Cloud databases is not allowed for assignment 1, you must use a local database installed on your Raspberry Pi. Use of Cloud databases is reserved for assignment 2.

The script should be scheduled to automatically run when the Pi boots

> You can use any means to run the script automatically, such as a cronjob, systemd service, having the file run on boot in the background, etc.

After saving to the database check if either the temperature or humidity are outside the
configured range and if so, push a notification using Pushbullet. Only send a maximum of 1
notification per day, i.e., don’t resend the notification every minute.

Hint: One way to achieve this is using the database to remember if you’ve already sent a
notification today.

### Task b (5 Marks)

Create a python file called `createReport.py` which will create a csv file called `report.csv`. This file should contain a separate row for each days’ data, additionally this data resides in the database. If each piece of data is within the configured temperature and humidity range then the status of OK is applied, otherwise the label of BAD is applied. An appropriate message detailing the error(s) is included. This script is executed manually to generate the report. Here is an example of `report.csv`:

```csv
Date,Status
09/03/2019,OK
10/03/2019,BAD: 5 *C below minimum temperature
11/03/2019,BAD: 10% above maximum humidity
```

### Task c (3 Marks)

Create a python file called `bluetooth.py` using Bluetooth to detect
nearby devices and when connected send an appropriate message stating the current
temperature, humidity and if these fall within the configured temperature and humidity
range.
This script should be scheduled to automatically run when the Pi boots.

### Task d (7 Marks)

Use 2 different Python data visualisation libraries to create 2 images (e.g., png files). This is where it gets interesting and you will need to do some research of your own.

You will now need to think:

- With the data that you have, what kind of data visualisation graph should be used? (Scatter plots, Bar charts and Histograms, Line plots, Pie charts, etc.)
- What should be represented in the above graph? Why did you make that decision?
- Python supports numerous data visualisation libraries. Which two libraries did you narrow it down to?

Create a python file called analytics.py that creates the above-mentioned images.
In addition to creating the images write a text file called analytics.txt comparing the different techniques used:

- Questions stated above and,
- an analytical comparison of the libraries used, advantages/disadvantages, simplicity/complexity, flexibility/configurations, anything you may think is necessary.

Use of JavaScript or any other language is prohibited for this task. You are only to use Python.

### Task e (5 Marks)

Professional use of a version control system and how the code has been developed over time. Please read the assignment rubrics for details.

You must use object-oriented python code (procedural code will fetch a **zero** for the
whole of assignment).

Note: You can add more python files in addition to the ones mentioned above.  
Note: Your code will be marked for its adherence to the PEP8 style guide for Python code.

## How and what to submit

Compress all files (or download branch as) zip, name of file is `<firstStudentNumber>_<secondStduentNumber>.zip` Incorrect names will incur a penalty.

Archive should contain:

- `config.json`
- `monitorAndNotify.py`
- `createReport.py`
- `bluetooth.py`
- `analytics.py`
- `analyticsReport.txt`
- any other files that are created.

## Contributors

- [Contributors](https://github.com/Volkor3-16/piot/graphs/contributors)

## License

- see [LICENSE](https://github.com/Volkor3-16/piot/blob/master/LICENSE.md) file

## Installation of Weather Services

1. Clone or download this branch. `git clone -b branchname`
2. Create a file called `token.json` in the following format Provided below and replace `<TOKEN>` with your generated Pushbullet access token.
3. Copy the systemd services. `sudo cp weathermonitor.service /etc/systemd/system/ && sudo cp weatherbluetooth.service /etc/systemd/system/`
4. Set Owner correctly. `sudo chown root:root /etc/systemd/system/weathermonitor.service && sudo chown root:root /etc/systemd/system/weatherbluetooth.service`
5. Set Permissions correctly `sudo chmod 644 /etc/systemd/system/weathermonitor.service && sudo chmod 644 /etc/systemd/system/weatherbluetooth.service`
6. reload, and start services `sudo systemctl daemon-reload && sudo systemctl start weathermonitor weatherbluetooth`
7. allow the services to start on boot. `sudo systemctl enable weathermonitor weatherbluetooth`

## token.json file format
```json
{
    "PB_api_token": "<TOKEN>"
}
``` 