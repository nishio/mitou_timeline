# -*- coding: utf-8 -*-
"""
Twitterをクロールしてファイルに保存
http://qiita.com/mima_ita/items/ba59a18440790b12d97e
"""

import twitter
import time
import secret

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

search_str="未踏 OR #mitou OR #mitoh"
RAW_FILE = "raw.txt"

api = twitter.Api(base_url="https://api.twitter.com/1.1",
                  consumer_key=secret.consumer_key,
                  consumer_secret=secret.consumer_secret,
                  access_token_key=secret.access_token_key,
                  access_token_secret=secret.access_token_secret)


def print_rate():
    rate = api.GetRateLimitStatus()
    print "Limit %d / %d" % (
        rate['resources']['search']['/search/tweets']['remaining'],
        rate['resources']['search']['/search/tweets']['limit'])
    tm = time.localtime(rate['resources']['search']['/search/tweets']['reset'])
    print "Reset Time  %d:%d" % (tm.tm_hour , tm.tm_min)


def crawl(last=None):
    """
    last: last id of previous search
    """
    print_rate()
    print "-----------------------------------------\n"

    if not last:
        found = api.GetSearch(term=search_str, count=100, result_type='recent')
    else:
        found = api.GetSearch(term=search_str, count=100, result_type='recent', max_id=last - 1)


    fo = file(RAW_FILE, "a")
    while True:
        for f in found:
            if last > f.id or last == None:
                last = f.id
            print f.text
            fo.write(
                "%s\t%s\t%s\n" %
                (f.text.replace("\n", "<br>"),
                 f.user.screen_name,
                 f.id)
            )

        if len(found) == 0:
            break
        print last
        found = api.GetSearch(term=search_str, count=100, result_type='recent', max_id=last - 1)

    print "-----------------------------------------\n"
    print_rate()

crawl()
