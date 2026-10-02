import json,re
def fx(t): return t.replace(' ? : ','—').replace(' ? ','—').replace(' : (',' (').replace(' : ','—')
p=r'E:/OneDrive/문서/GitHub/uui-resources/book/book.js'
s=open(p,encoding='utf-8').read(); d=json.loads(s[s.index('(')+1:s.rindex(')')])
for P in d['papers']:
    P['title']=fx(P['title'])
    for S in P['sections']: S['title']=fx(S['title'])
open(p,'w',encoding='utf-8').write('UB_BOOK('+json.dumps(d,ensure_ascii=False,separators=(',',':'))+');')
q=r'E:/OneDrive/유란시아 작업/uui-en/en_texts.json'
T=json.load(open(q,encoding='utf-8'))
for k,v in T.items():
    v['title']=fx(v['title']); v['sections']={a:fx(b) for a,b in v['sections'].items()}
json.dump(T,open(q,'w',encoding='utf-8'),ensure_ascii=False)
print([t for v in T.values() for t in [v['title']]+list(v['sections'].values()) if '?' in t or ' : ' in t])
