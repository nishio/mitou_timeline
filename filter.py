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

sort_with_score()
