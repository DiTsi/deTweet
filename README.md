# deTweet
Automatically delete your Twitter posts

## Features
- human-like removing (no limits)
- delete tweets, replies, retweets
- delete within specific date range

## Limitations
- works only with plain nickname-password authentication

## How to use
- Download your Twitter `archive` from [here](https://twitter.com/settings/download_your_data)
- Git clone this project with `git clone git@github.com:DiTsi/deTweet.git`
- Copy `deTweet/env-default.txt` to `deTweet/.env` and set [environment variables](#environment-variables)
- Get file `data/tweets.js` from Twitter archive and put it to `deTweet/` root directory
- Go to `deTweet/` directory and run:
  ```bash
  python -m venv env
  source env/bin/activate
  pip install requirements.txt
  python main.py
  ```

## Environment variables
|Name|Description|Example|
|-|-|-|
|AUTOSTART|Start delete process without questions|False|
|BACKUP_PATH|Path to `tweets.js` file|./tweets.js|
|MAX_ATTEMPTS|Max number of delete attempts|3|
|NICKNAME|Your nickname without '@'|NickName|
|PASSWORD|Your account password|password|
|START_DATE|Start date for data range|2000-01-31|
|STOP_DATE|Stop date for data range|2030-06-30|
|TIMEZONE|Your local TZ identifier (see [list](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones))|Asia/Tashkent|
|WAIT|Max seconds waiting for elements, sec|10|
