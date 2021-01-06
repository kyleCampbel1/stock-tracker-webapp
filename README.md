Server for webapp to track stock prices and report metrics to users.

System was running Python 3.7.7 on MacOS.

To launch in dev mode (recommended):
After creating your venv, run  pip install -r requirements.txt. Edit the config.py file and insert your secret key. On the commandline, The command 'flask run' will locally run the development version of the app - production is not currently configured. On the command line, run flask shell and from there enter the commands which are in the file 'createDB.py'. 

In order to initiate querying the cryptowatch API for market data each minute the following commands should be run (on Unix based systems). 
1. crontab -e
2. edit the script to have '* * * * * cd /<project directory> && /<project directory>/.venv/bin/flask crypto >>cw.log 2>&1'
If you are on MacOS, you will likely need to go to Settings/Security and Privacy/Privacy/Full Disk Access, click the + to add applications with access and use cmd+shift+g to access /usr/sbin/cron. Windows should refer to creating a scheduled task to execute the flask crypto command.
Refer to https://github.com/cryptowatch/cw-sdk-python#setup-your-credential-file for instructions on how to create a paid Cryptowatch account and API key for increased request allowance.

For sanity checks, I used the webservice Postman to send requests to the REST API. Because signup and login redirect you, PostMan displays the response to those redirect pages which is a 405, but in your editor (VSCode) you will see the requests go through. General Postman workflow. A user should signup and then login using something of the form {"email":"address","password":"1234"}. Once logged in, a user may add metrics with a JSON of the form {"ticker":"btcusdt","exchange":"binance"}. A complete list of valid exchanges and tickers can be found at https://api.cryptowat.ch/markets. 

To view changes in the database, at the terminal run: sqlite3 dev.db and from there you can query as desired. 

Testing:
Running in test mode:
The current functionality of the unit tests are limited, and they will likely end in failure. However, running python3 -m unittest tests/<testFile>.py will run the specific testfile. I will be improving the robustness of these tests going forwards. I struggled to find resources on granting test application context, as many endpoints require a user to be logged-in, meaning I have not yet been able to test those.
  
How testing should be further expanded:
I will finish making unit tests for each endpoint of the API and for the accessory functions. We can also add testing for the status codes. Currently, there isn't testing for faulty inputs, so I will devise ways to handle invalid inputs and expand testing for them. I shoul make automated tests to simulate numerous users and metrics and tracking response time. Adding integration tests to ensure the Cryptowatch API works dependably is also a priority.

Architecture:

The API is currently very simple and supports User: registration (POST), logging in (POST), and logging out (GET). Once a user is authenticated, they may add a market to track (POST), view a metric's 1-day history (GET), stop tracking a metric (DELETE), view their metrics ranked against each other (GET), view their metrics (GET)

The respective endpoints are: /signup, /login, /logout, /add_metric, /<ticker>_<exchange>_day_view, /remove_metric, /metric_rankings, /my_markets
  
The database uses Flask-SQLAlchemy on top of SQLite to provide the advantages of ORM to relate Users to their Metrics and vice versa. The actively managed tables corresponding to classes are User, Metric, Markets. Markets contains a list of the unique exchange and currency pairs across all of the users. Metric contains price and other historical market data on these markets. Metric is updated each minute with data from the Cryptowatch REST API. Naturally, User contains the users. Due to the relationships imposed between these tables, when a user adds a metric, we can add it to their list of metrics, and they will be related to a unique Market in Markets, which will be created, if it does not already exist. Likewise, each market has a list of users which view it, which is automatically updated when a market is associated to a user. Additionally, each market is related to all of the metrics which track its history. This makes getting history for a metric, sending email alerts to all users interested in a particular metric, and displaying information for all of a users metrics a relatively fast search.

Using Click, I defined a custom command, which using cron as specified above will query the Cryptowatch API each minute for new market data. This is advantageous over threading implementations because the flask command has access to the app's context, without the need to pass information back and forth, and can directly update the database. It also does not interrupt the app's ability to process user requests. 


Scalability:
Immediate features to add for scaling would be a process that clears the Metric table of data that is over 1 day old. Currently, if a user requests their metric ranking, all of their metric data from the past 24 hours is queried, and the standard deviation for each metric is computed. If many users were to request this, and they shared common metrics, it might be better to compute the rankings at regular intervals for all metrics, and then filter an ordered sublist with only the metrics relevant to each user upon request. I could also use Celery to offload requests or load balancers. 

If the number of metrics to track increased, and the frequency of querying them increased, I think distributing the requirements with a server for each metric could be scalable. Creating a table and class for each metric could also lead to query improvements. I also think that creating modules to stop computing the 1 hr average of each metric every time a metric is queried and instead compute the change based on the additional observed datapoint would reduce computational load. 

Monitoring:
For monitoring, I would add log files to notify the server maintainer if a certain number of requests fail within a certain time period, and log all errors clients receive. I would also need to add monitoring to the cron job to ensure that market data is collected on schedule. Creating monitoring on the database, to ensure that the tables are of expected size and parameters. I would also monitor average response time and user volume throughout the day. Random tests of selecting a user and performing queries to the API and comparing expected output to API response could also be of use.
