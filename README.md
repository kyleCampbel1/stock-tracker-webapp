Server for webapp to track stock prices and report metrics to users.

Requirements (via pip install):
flask,
flask-sqlalchemy,
cryptowatch-sdk,

System was running Python 3.7.7 on MacOS.

Refer to https://github.com/cryptowatch/cw-sdk-python#setup-your-credential-file for instructions on how to create a paid Cryptowatch account and API key for increased request allowance.


Metric rankings could be computed across all metrics for all users and then filter the displayed metrics by each user.
Could create tables in database for each market if searching for the instances of each market in the Metric table became too expensive as the number of markets increases.

Are cookies secure enough for user data? -- probably

concurrency issues