import json,re
t=open(r'E:/OneDrive/내 문서/유란시아/내번역 최종/urantia_eng.txt',encoding='cp949',errors='replace').read().splitlines()
d=json.load(open(r'C:/Users/WIN10/AppData/Local/Temp/claude/reader_en_data.txt',encoding='utf-8'))
R={}
for p in d:
  for s in p['sections']:
    for q in s['paras']:
      x=q['text'].replace('---','—').replace(chr(92)+'[','[').replace(chr(92)+']',']')
      x=re.sub(r'\^(\w+)\^',r'<sup>\1</sup>',x)
      R[q['ref']]=x
def key(x): return re.sub(r'[^A-Za-z0-9]','',re.sub(r'<sup>(\w+)</sup>',r'\1',x))
papers=[];cur=None;sec=None;used=fixed=0;left=[]
for l in t[2:]:
  l=l.strip()
  if not l: continue
  m=re.match(r'(\d+):(\d+)\.(\d+) (.*)',l)
  if m:
    ref=f'{m[1]}:{m[2]}.{m[3]}'; txt=m[4]
    r=R.get(ref)
    if r and key(r)==key(txt): txt=r; used+=1
    else:
      txt=re.sub(r' \? ','—',txt); txt=re.sub(r' \?(?=[,.;:’”]|$)','—',txt); txt=txt.replace('attach?s','attachés'); fixed+=1
      if '?' in txt and re.search(r'(?<![\w’”)])\?|\?(?=\w)',txt): left.append(ref)
    if sec is None or int(m[2])!=sec['sec']:
      sec={'sec':int(m[2]),'title':'','paras':[]}; cur['sections'].append(sec)
    sec['paras'].append({'cit':ref,'text':txt}); continue
  if l=='Foreword': cur={'no':0,'title':'Foreword','sections':[]}; papers.append(cur); sec=None; continue
  pm=re.match(r'Paper (\d+)\s*:\s*(.*)',l)
  if pm: cur={'no':int(pm[1]),'title':pm[2],'sections':[]}; papers.append(cur); sec=None; continue
  pend=l  # section heading — attach to the next section
  n=len(cur['sections'])
  sec={'sec':-1,'title':l,'paras':[]}
  # resolve sec number lazily
  cur['sections'].append(sec)
# merge heading placeholders: heading sections with sec -1 get number of first para
for p in papers:
  out=[]
  for s in p['sections']:
    if s['sec']==-1: out.append(s); continue
    if out and out[-1]['sec']==-1 and not out[-1]['paras']:
      out[-1]['sec']=s['sec']; out[-1]['paras']=s['paras']
    else: out.append(s)
  p['sections']=[s for s in out if s['paras']]
n=sum(len(s['paras']) for p in papers for s in p['sections'])
print('papers',len(papers),'paras',n,'from reader',used,'heuristic',fixed,'suspect',len(left),left[:10])
print(papers[1]['sections'][1]['title'], papers[139]['sections'][9]['title'])
open('book.js','w',encoding='utf-8').write('UB_BOOK('+json.dumps({'papers':papers},ensure_ascii=False,separators=(',',':'))+');')
