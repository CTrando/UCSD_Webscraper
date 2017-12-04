# Purpose

This is a project that is designed to reduce some of the thinking during class enrollment with UCSD's web registration app, WebReg.

# Demo

![demo_img_1](https://raw.githubusercontent.com/CTrando/UCSD_Webscraper/master/images/demo_img_1.PNG?token=ARZ14si_r85T1ErEwUkGFv3Tnx7DMsaYks5Z9Q_UwA%3D%3D)
![demo_img_2](https://raw.githubusercontent.com/CTrando/UCSD_Webscraper/master/images/demo_img_2.PNG?token=ARZ14i604cNYi8ylYbQS7vVTpRom0CWVks5Z9RAFwA%3D%3D)


This should work with most regular type classes (lectures,
discussions, seminars, finals, etc).


# Process
The idea is to use a webscraper that will login to WebReg and search through every class in every department, storing that locally.

From there, I created a GUI which will take in a list of desired classes as well as a list of preferred times, and the program will try and select classes in those time periods, creating the best schedule possible from the specifications.

# Technologies
This project was written exclusively in Python.
* [Selenium](http://www.seleniumhq.org/) to navigate through WebReg and download information
* [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/) to parse the HTML
* [Sqlite3](https://docs.python.org/2/library/sqlite3.html) to interact with a SQLite database
* [Kivy](https://kivy.org/#home) to create the GUI


# In Depth Process
UCSD requires a login to access any data, so that is achieved through using Selenium to enter in information into the username and password field and login.

UCSD masks most of its class data on WebReg, requiring a click event to get new HTML from its server, but with Python Selenium, I are able to simulate a user click on each class, thereby aquiring all the HTML which we download, parse, clean, and put into a SQLite database.

From there, I get user input for the list of classes, and I get all the classes with the same course number as the inputs from my database. I then use depth first search with backtracking to select my classes and evaluate them on overall fitness (how well they fit within the given time periods, if they overlap, etc.).

At the end, I return the best class set.

# Instructions

Clone the repository into a folder with:

`git clone https://github.com/CTrando/UCSD_Webscraper.git`

Navigate to that folder.

To install the necessary libraries, run ```pip install -r libs.txt``` from a terminal or console. Wait until all the libraries have finished installing.

To run the program, run:
`python gui.py` in the terminal or some equivalent IDE.

That is where the GUI code is held which references the other part of the program. A GUI should appear, however you will be unable to generate classes until you scrape the classes yourself.

To keep the size of the install small and protect private information as well as for possible legal concerns, you will have to download and webscrape the classes yourself.

At the moment, **webscraping will only work with Google Chrome**. If you want to use a different browser, you must look up the corresponding Selenium webdriver application and edit the `scraper.py` file.

**Skip if you are using Chrome**

Download:

* Firefox [geckodriver](https://github.com/mozilla/geckodriver/releases)
* Safari [safaridriver](https://github.com/SeleniumHQ/selenium/wiki/SafariDriver)
* etc.

Put the webdriver exe file into the `drivers` folder.
Now go into `scraper.py` in the `scraper` directory and change the `Chrome` constructor to the corresponding constructor.

**End Skip**

Click on the webscrape data and enter in your username and password for WebReg.

### Do so at your own risk! I cannot guarantee the safety of your information.

After that, the application should begin webscraping WebReg. It will take a while to get every department, however it can be started and stopped at any time.

**At the moment, there are a few bugs with the GUI interface for web scraping.**

If and when the webscraping finishs, you should be able to add your classes to the application and click `Begin` to generate yourself a schedule!

**I understand the webscraping is slow, I will work on a better solution.**


# Contributors #

If you want to contribute, I'd be glad to have the help. Right now, the current features I want to add are:

* A calendar viewing option for the generated classes
* Adding more preferences
* Switching the background images possibly
* Making the class type database dynamic
* Improving class selection speed


# Final Notes #

If you made it this far, thanks for reading! Leave a star if you enjoyed!








