import codecs
import features

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

def get_last_data():
    import os
    ws = os.listdir('week_data')
    ws.remove('README.md')
    ws.sort()
    return ws[-1]

def output_html():
    last_data = get_last_data()
    print 'processing:', last_data
    fi = file('week_data/' + last_data)
    from lr import learn, make_feature_matrix
    lr = learn()

    lines = fi.readlines()
    X = make_feature_matrix(lines)
    ps = lr.predict_proba(X)[:, 1]

    data = []
    for line, p in zip(lines, ps):
        if line.startswith("RT "): continue
        if p < 0.4: continue
        print line
        print p
        items = line.split('\t')
        url = "https://twitter.com/{1}/status/{2}".format(*items)
        data.append(dict(url=url, score=p))
    print len(data)
    render(data, last_data)

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

output_html()
