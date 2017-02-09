Android Play Store: Reviews autoreply

Automatically reply to Google Play Store user reviews using the Publisher API and OAuth2.

The script is intended to run as a cronjob. On each run, it will check the latest 50 reviews and reply a canned response (from replyToReview method, universalCannedResponse variable ) to every review that has fewer than 5 stars.

## Installation

The script is a python2 file.

1. Download Google APIs Client Library for Python (google-api-python-client):
  https://code.google.com/p/google-api-python-client/

  or use pip:

  ```bash
  $ pip install google-api-python-client
  ```

  You may need to use `pip2` instead of `pip`.

2. Make sure you can import the client library:

  ```bash
  $ python
  >>> import apiclient
  >>>
  ```

  You may need to use `python2` instead of `python`

## First request using OAuth2: Installed application

1. Edit the `client_secrets.json` file and add the client ID and client secret.

2. Execute any of the scripts to begin the auth flow:

  ```bash
  $ python basic_list_apks.py com.myapp.package
  ```

  A browser window will open and ask you to login. Make sure the account has
  enough permissions in the Google Play Developer console.

3. Accept the permissions dialog. The browser should display

  `The authentication flow has completed.`

  Close the window and go back to the shell.

4. The script will output a list of apks.

5. The tokens will be stored in `androidpublisher.dat`. Remove this file to restart the
 auth flow.


## Running as a cronjob

SSH to your server and `crontab -e` to edit the crontab.

Before running the script for the first time, you need to go through the auth routine, which is a bit more complicated when running from a cronjob.

Add the following entry to get cron environment variables into a file:

```* * * * * export -p > ~/cron-env```

and let it run once. Then remove the line.
You should now have a cron-env file in your home directory.
You can then run:

```cd && env -i sh -c '. ./cron-env; exec bash'```

Now you are in a cron environment shell. Run the reply-to-reviews.py script and go through the auth flow. After that, your script cronjob will work. Let's add it:

Sample crontab entry would be:

```  */5 *  *   *   *     /usr/bin/python2 /home/username/reply-to-reviews/reply_to_reviews.py com.package.name >> /home/username/reply-to-reviews.log```

This will run the script every 5 minutes and also log to a logfile, which you can check using `tailf /home/username/reply-to-reviews.log`.
