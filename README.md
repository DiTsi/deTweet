# deTweet
Automatically delete your Twitter posts

## Features
- human-like removing (no limits)
- delete tweets, replies, retweets
- delete within specific date range

## Limitations
- works only with plain nickname-password authentication

## How to use
There are two options: using Docker (simple) and using source code

### Docker
- create `docker-compose.yml` file, paste content below and set your environment variables
  ```yaml
  version: "3.7"
  services:
    detweet:
      image: ghcr.io/ditsi/detweet:main
      environment:
        NICKNAME: "NickName"
        PASSWORD: "password"
        TIMEZONE: "Asia/Tashkent"
        START_DATE: "2006-03-21"
        STOP_DATE: "2030-06-30"
        DELETE_TWEETS: "True"
        DELETE_REPLIES: "True"
        DELETE_RETWEETS: "True"
  
        AUTOSTART: "True"
        BACKUP_PATH: "/tweets.js"
        HEADLESS: "True"
        STATUS_PATH: "/status"
        MAX_ATTEMPTS: "3"
        WAIT: "15"
      volumes:
        - ./tweets.js:/tweets.js:ro
        - ./status:/status
  ```
- run `docker-compose up`

### Source code
- download your Twitter `archive` from [here](https://twitter.com/settings/download_your_data)
- git clone this project with `git clone git@github.com:DiTsi/deTweet.git`
- copy `deTweet/env-default.txt` to `deTweet/.env` and set [environment variables](#environment-variables)
- get file `data/tweets.js` from Twitter archive and put it to `deTweet/` root directory
- go to `deTweet/` directory and run:
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
|DELETE_TWEETS|Delete tweets|True|
|DELETE_REPLIES|Delete replies|True|
|DELETE_RETWEETS|Delete retweets|True|
|HEADLESS|Run Firefox without interface|False|
|STATUS_PATH|Path to status directory|./status|
|MAX_ATTEMPTS|Max number of delete attempts|3|
|NICKNAME|Your nickname without '@'|NickName|
|PASSWORD|Your account password|password|
|START_DATE|Start date for data range|2006-03-21|
|STOP_DATE|Stop date for data range|2030-06-30|
|TIMEZONE|Your local TZ identifier (see [list](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones))|Asia/Tashkent|
|WAIT|Max seconds waiting for elements, sec|10|
