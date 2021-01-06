Server for webapp to track stock prices and report metrics to users.

System was running Python 3.7.7 on MacOS.

Refer to https://github.com/cryptowatch/cw-sdk-python#setup-your-credential-file for instructions on how to create a paid Cryptowatch account and API key for increased request allowance.


Metric rankings could be computed across all metrics for all users and then filter the displayed metrics by each user.
Could create tables in database for each market if searching for the instances of each market in the Metric table became too expensive as the number of markets increases.

concurrency issues


Run api.createDB.py after the initial download. Create your own private key in the debug_environment.cfg
The command 'flask run' will locally run the development version of the app - production is not currently configured. You can use the webservice Postman to send requests to the REST API. Because signup and login redirect you, PostMan makes it seems like your requests are invalid, but in your editor (VSCode) you will see the requests go through.

More confirmation the requests are valid can come from running sqlite3 api/cryptoDatabase.db from the terminal and then querying to view your changes.
Fully removing any object (User, Market, Metric) from a table has not yet been implemented into the API. However, a user may remove a metric from their specific list of metrics. A user should add metrics with a JSON of the form {"ticker":"btcusdt","exchange":"binance"}. A complete list of valid exchanges and tickers can be found at https://api.cryptowat.ch/markets. 

In order to initiate querying the cryptowatch API for market data each minute the following commands should be run (on Unix based systems). 
1. crontab -e
2. edit the script to have '* * * * * cd /<project directory> && /<project directory>/.venv/bin/flask crypto >>cw.log 2>&1'
If you are on MacOS, you will likely need to go to Settings/Security and Privacy/Privacy/Full Disk Access, click the + to add applications with access and use cmd+shift+g to access /usr/sbin/cron. Windows should refer to creating a scheduled task to execute the flask crypto command.

