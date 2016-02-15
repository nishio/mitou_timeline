# -*- coding: utf-8 -*-
"""
Twitterを毎分継続的にクロール
"""

import twitter
import time
import secret
from lr import learn, make_feature_matrix

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

search_str="未踏 OR #mitou OR #mitoh"
OUT_FILE = time.strftime('data/%Y%m%d_%H%M.txt')

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


def crawl(last=None, previous_latest=None):
    """
    last: last id of previous search
    """
    print_rate()
    print "-----------------------------------------\n"

    if not last:
        found = api.GetSearch(term=search_str, count=100, result_type='recent')
    else:
        found = api.GetSearch(term=search_str, count=100, result_type='recent', max_id=last - 1)

    buf = []
    latest_id = found[0].id
    while True:
        for f in found:
            if last > f.id or last == None:
                last = f.id
            if previous_latest and f.id < previous_latest:
                # already crawled zone
                break
            #print f.text
            if f.retweeted_status:
                retweeted_id = f.retweeted_status.id
            else:
                retweeted_id = 0

            data = "%s\t%s\t%s\t%s\t%s\t%s\n" % (
                f.text.replace("\n", "<br>"),
                f.user.screen_name,
                f.id,
                f.retweet_count,
                f.favorite_count,
                retweeted_id,
            )
            buf.append(data)

        if len(found) == 0:
            break
        print last
        if last < previous_latest: break
        found = api.GetSearch(term=search_str, count=100, result_type='recent', max_id=last - 1)

    # bufはnew->old順になっている。
    buf.reverse()

    fo = file(OUT_FILE, "a")
    for line in buf:
        fo.write(line)
    fo.close()
    print "-----------------------------------------\n"
    print_rate()
    return latest_id


def output_html(lr):
    fi = file(OUT_FILE)

    lines = []
    used = []
    for line in fi:
        if line.startswith("RT "): continue
        if any(line.startswith(x) for x in used):
            continue
        used.append(line[:30])
        lines.append(line)
    lines.reverse()

    X = make_feature_matrix(lines)
    ps = lr.predict_proba(X)[:, 1]

    data = []
    for line, p in zip(lines, ps):
        if p < 0.6: continue
        items = line.split('\t')
        url = "https://twitter.com/{1}/status/{2}".format(*items)
        data.append(dict(url=url, score=p, text=items[0]))
    print len(data)
    from filter import render
    render(data, OUT_FILE)


def main():
    lr = learn()
    latest_id = crawl()
    output_html(lr)
    while True:
        time.sleep(60)
        try:
            latest_id = crawl(previous_latest=latest_id)
        finally:
            print 'latest:', latest_id
            print 'rendering'
            output_html(lr)
            print 'rendered'
main()
