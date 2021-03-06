import codecs
import features
import argparse

def find_neutral():
    fi = file('raw.txt')
    for line in fi:
        if line.startswith('RT '): continue
        if any(x in line for x in features.NEGATIVE): continue
        if any(x in line for x in features.POSITIVE): continue
        print line

def sort_with_score():
    fi = file('raw.txt')
    buf = []
    for line in fi:
        if line.startswith('RT '): continue
        score = 0
        for x in features.NEGATIVE:
            if x in line: score -= 1
        for x in features.POSITIVE:
            if x in line: score += 1
        buf.append((score, line))

    buf.sort(reverse=True)
    for score, line in buf:
        print score, line

#sort_with_score()

def get_target_file():
    if args.target_file:
        return args.target_file
    import os
    ws = os.listdir('week_data')
    ws.remove('README.md')
    ws.sort()
    return 'week_data/' + ws[-1]

def output_html():
    target_file = get_target_file()
    print 'processing:', target_file
    fi = file(target_file)
    from lr import learn, make_feature_matrix
    lr = learn()

    lines = fi.readlines()
    X = make_feature_matrix(lines)
    ps = lr.predict_proba(X)[:, 1]

    data = []
    for line, p in zip(lines, ps):
        if line.startswith("RT "): continue
        if p < args.threshold: continue
        if p > args.upper_limit: continue
        items = line.split('\t')
        url = "https://twitter.com/{1}/status/{2}".format(*items)
        data.append(dict(url=url, score=p, text=items[0]))
    print len(data)
    render(data, target_file)


def render(data, filename):
    from jinja2.environment import Environment
    from jinja2 import Template, FileSystemLoader
    env = Environment()
    env.loader = FileSystemLoader('.')
    t = env.get_template('template.html')
    html = t.render(data=data, filename=filename)
    fo = codecs.open('output.html', 'w', 'utf-8')
    fo.write(html)
    fo.close()


def add_train_data():
    target_file = get_target_file()
    print 'processing:', target_file
    fi = file(target_file)
    from lr import learn, make_feature_matrix
    lr = learn()

    lines = fi.readlines()
    X = make_feature_matrix(lines)
    ps = lr.predict_proba(X)[:, 1]

    data = []
    for line, p in zip(lines, ps):
        if line.startswith("RT "): continue
        if p < args.threshold: continue
        if p > args.upper_limit: continue
        print line
        print p
        items = line.split('\t')
        url = "https://twitter.com/{1}/status/{2}".format(*items)
        print url
        ret = raw_input("negative(z), neutral(x), positive(c)>")
        if ret == 'c':
            fo = file('positive.txt', 'a')
            fo.write(line)
            fo.close()
        elif ret == 'z':
            fo = file('negative.txt', 'a')
            fo.write(line)
            fo.close()
        print


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='filter mitoh tweets')
    parser.add_argument('--output-html', action='store_true')
    parser.add_argument('--add-train-data', action='store_true')
    parser.add_argument('--target-file')
    parser.add_argument('--threshold', type=float, default=0.5)
    parser.add_argument('--upper-limit', type=float, default=1.0)
    args = parser.parse_args()

    if args.add_train_data:
        add_train_data()

    if args.output_html:
        output_html()

    if not args.output_html and not args.add_train_data:
        # if nothing are specified:
        output_html()
