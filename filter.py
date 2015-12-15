import features

def find_neutral():
    fi = file('raw.txt')
    for line in fi:
        if line.startswith('RT '): continue
        if any(ng in line for ng in features.NG_WORDS): continue
        if any(ng in line for ng in features.NEGATIVE): continue
        if any(ng in line for ng in features.POSITIVE): continue
        print line

find_neutral()
