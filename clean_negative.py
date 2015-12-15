import re
lines = file('negative.txt').readlines()
print len(lines)
buf = []
used = []
for line in lines:
    line = re.sub('https:[^\s]+', 'URL', line)
    text = line.split('\t')[0]
    if text not in used:
        used.append(text)
        buf.append(line)

print len(buf)
file('negative.txt', 'w').write(''.join(buf))
