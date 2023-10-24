## Project Information
This project allows user to scrape websites. Currently scrapes https://www.skonis-kvapas.lt/arbata/juodoji-arbata, but could be configured to scrape multiple pages at once.
Scrapes only indicated data from websites, so depending on the website and data in it, recommended to configure Scraper.py file.

## Libraries/Frameworks/Modules
### This project uses:

* Requests
* Mysql.connector
* Beautifullsoup(BS4)
* Time
* Random

## Using the Scraper
Install all dependencies, inside Scraper.py file call "printing_data" function and watch information flowing into the database. \
P.s in order to run it you need to configure Scraper.py file and connect it to your database,
if you don't want to save data, just comment out function "Saving_data".