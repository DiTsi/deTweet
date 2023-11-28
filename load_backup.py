import json


def tweets_list(json_path="./tweets.js"):
    with open(json_path, 'r') as f:
        content = f.read()
    content = content.replace('window.YTD.tweets.part0 = ', '')
    tweets = json.loads(content)
    for t in tweets:
        yield t['tweet']
