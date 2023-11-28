# deTweet
Automatically delete all your Twitter information

## Features
- Automatically delete all your retweets
- Automatically delete all your replies
- Automatically delete all your tweets

## How to use
1. Download your Twitter `archive` from [here](https://twitter.com/settings/download_your_data)
2. Git clone this project with `git clone git@github.com:DiTsi/deTweet.git`
3. Copy `deTweet/env-default.txt` to `deTweet/.env` and place actual info into it
4. Put file `data/tweets.js` from Twitter archive to `deTweet/` root directory
5. Go to `deTweet/` directory and run `yarn && yarn start data/tweets.js`

## Problems
### Slow Internet
If you have problems with delays on slow internet connection, you can manually change delays in `src/index.ts` (8-11 lines)

