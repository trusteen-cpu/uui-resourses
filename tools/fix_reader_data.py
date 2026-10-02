import re, json, gzip, base64, sys
p = sys.argv[1]
s = open(p, encoding='utf-8').read()
b = open(r'E:/OneDrive/문서/GitHub/uui-resources/book/book.js', encoding='utf-8').read()
B = json.loads(b[b.index('(') + 1:b.rindex(')')])
out = []
for P in B['papers']:
    secs = []
    for S in P['sections']:
        t = re.sub(r'^\d+\.\s*', '', S['title'] or '')
        secs.append({"num": S['sec'], "title": t,
                     "paras": [{"ref": q['cit'], "text": re.sub(r'<sup>(\w+)</sup>', r'\1', q['text'])} for q in S['paras']]})
    out.append({"num": P['no'], "title": P['title'], "sections": secs})
# find the old blob and check its shape
blobs = list(re.finditer(r'(["\'`])([A-Za-z0-9+/=]{5000,})\1', s))
assert len(blobs) == 1, len(blobs)
m = blobs[0]
old = json.loads(gzip.decompress(base64.b64decode(m.group(2))).decode('utf-8'))
print('old', len(old), 'new', len(out), 'old sec0 title sample:', old[1]['sections'][1]['title'])
new_b64 = base64.b64encode(gzip.compress(json.dumps(out, ensure_ascii=False, separators=(',', ':')).encode('utf-8'), 9)).decode()
s = s[:m.start(2)] + new_b64 + s[m.end(2):]
open(p, 'w', encoding='utf-8').write(s)
print('ok', sum(len(x['paras']) for P in out for x in P['sections']))
