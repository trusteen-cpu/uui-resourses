import re, json, sys
T = json.load(open(r'E:/OneDrive/유란시아 작업/uui-en/en_texts.json', encoding='utf-8'))
C = {}
for v in T.values():
    for line in v['text']:
        m = re.match(r'(\d+:\d+\.\d+)\s+(.*)', line)
        C[m.group(1)] = m.group(2)
p = sys.argv[1]
s = open(p, encoding='utf-8').read()
n = 0
def rep(m):
    global n
    k = m.group(1)
    if k in C:
        n += 1
        return '"%s":%s' % (k, json.dumps(C[k], ensure_ascii=False))
    return m.group(0)
s = re.sub(r'"(\d+:\d+\.\d+)":"((?:[^"\\]|\\.)*)"', rep, s)
print('replaced', n)
for k in ['¡°', '¡±', '¡¯', '¡®', '¡Æ', ' ? ']:
    print(repr(k), s.count(k))
open(p, 'w', encoding='utf-8').write(s)
