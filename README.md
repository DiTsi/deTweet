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
- Get file `data/tweets.js` from Twitter archive and place it to `deTweet/` root directory
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
|NICKNAME|Your nickname without '@'|NickName|
|PASSWORD|Your account password|password|
|BACKUP_PATH|Path to `tweets.js` file|./tweets.js|
|START_DATE|Start date for delete range|2022-06-16|
|STOP_DATE|Stop date for delete range|2023-07-17|
|TIMEZONE|Your local TZ identifier (see [list](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones))|Asia/Tashkent|
|AUTOSTART|Start delete process without questions|False|
