import re
src = open(r'E:/OneDrive/문서/GitHub/urantia-portal/textapp/index.html', encoding='utf-8').read()
css = src[src.index('<style>'):src.index('</style>') + 8]
css = css.replace('"Noto Serif KR","Nanum Myeongjo",Georgia,"맑은 고딕",serif', 'Georgia,"Times New Roman",serif').replace('text-align:justify;word-break:keep-all', 'text-align:left;hyphens:auto')
css = css.replace('.pa .c{flex:0 0 60px', '.pa .c{flex:0 0 66px')
css = css.replace('</style>', '''.res{margin:0 0 14px;padding:10px 12px;border:1px solid var(--line);border-radius:10px;background:var(--card);cursor:pointer;line-height:1.7}
.res:hover{border-color:var(--gold)}.res b{color:var(--gold);font-size:12.5px}.res mark{background:rgba(201,162,39,.35);color:inherit}
</style>''')
js = src[src.index('<script>\nvar BOOK'):]
R = [
    ("u.lang='ko-KR'", "u.lang='en-US'"),
    ("/^ko/i.test(v.lang)", "/^en/i.test(v.lang)"),
    ("var FEM=/sunhi|heami|female|google 한국|google korean|여성/i, MAL=/injoon|hyunsu|male|남성/i;",
     "var FEM=/aria|jenny|zira|samantha|female|susan|hazel|libby|sonia/i, MAL=/guy|david|mark|daniel|male|ryan|george|christopher|eric/i;"),
    (".replace(/\\s*-\\s*Korean.*$/i,'').replace(/Online\\s*\\(Natural\\)/i,'자연스러움')", ".replace(/Online\\s*\\(Natural\\)/i,'Natural')"),
    ("' · 여':(MAL.test(v.name)?' · 남':'')", "' · F':(MAL.test(v.name)?' · M':'')"),
    ("o0.textContent='기본 음성 (어느 브라우저나 같음)'", "o0.textContent='Standard voice (same in every browser)'"),
    ("tl=ko", "tl=en"),
    ("/[「」『』\\[\\]—―]/g", "/[\\[\\]—―]/g"),
    ("$('#playch').textContent='▶ 듣기'", "$('#playch').textContent='▶ Listen'"),
    ("$('#playch').textContent='⏸ 멈춤'", "$('#playch').textContent='⏸ Pause'"),
    ("('제'+p.no+'편 '+p.title).indexOf(f)>=0", "('paper '+p.no+' '+p.title).toLowerCase().indexOf(f.toLowerCase())>=0"),
    ("f&&(s.title||'').indexOf(f)>=0", "f&&(s.title||'').toLowerCase().indexOf(f.toLowerCase())>=0"),
    ("(p.no===0?'머리말':'제'+p.no+'편')", "(p.no===0?'Fwd':p.no)"),
    ("(s.sec===0?'머리글':'제'+s.sec+'장')", "(s.sec===0?'Introduction':'Section '+s.sec)"),
    ("찾은 것이 없습니다.", "No titles match. Press Enter to search the full text."),
    ("(p.no===0?'머리말':'제 '+p.no+' 편')", "(p.no===0?'FOREWORD':'PAPER '+p.no)"),
    ("esc(q.text)+", "fmt(q.text)+"),
    ('title="이 절 듣기"', 'title="Listen to this paragraph"'),
    ('<button id="prev">← 이전 장</button><button id="nextb">다음 장 →</button>', '<button id="prev">← Previous</button><button id="nextb">Next →</button>'),
    ("$('#home').onclick=function(){location.href='/'};", "$('#home').onclick=function(){location.href='../'};"),
    ("본문을 불러오지 못했습니다. 인터넷 연결을 확인하신 뒤 이 쪽을 다시 열어 주세요.", "The text could not be loaded. Please check your connection and reload this page."),
    ("/* 구글 음성은 한 번에 190자까지 */", "/* the standard voice takes up to 190 characters at a time */"),
    ("/* 구글 음성이 막히면 브라우저 음성으로 */", "/* if the standard voice is blocked, fall back to a browser voice */"),
    ("/* ---------- 목소리 ---------- */", "/* ---------- voices ---------- */"),
    ("/* ---------- 낭독 ---------- */", "/* ---------- reading aloud ---------- */"),
    ("/* ---------- 화면 ---------- */", "/* ---------- screen ---------- */"),
    ("// 장이 끝났을 때", "// end of section"),
    ("/* 주소 끝 #107:0.2 처럼 절 번호가 있으면 그 절로 바로 간다 */", "/* #107:0.2 at the end of the address jumps straight to that paragraph */"),
]
for a, b in R:
    assert a in js, a[:60]
    js = js.replace(a, b)
js = js.replace("(s.sec===0?'머리글':'제'+s.sec+'장')", "(s.sec===0?'Introduction':'Section '+s.sec)")
js = js.replace("'ub_", "'ube_")
i = js.index('function showNote(){'); j = js.index('/* #107:0.2')
js = js[:i] + "function showNote(){}\n" + js[j:]
js = js.replace("function esc(t){", "function fmt(t){return esc(t).replace(/&lt;sup&gt;(\\w+)&lt;\\/sup&gt;/g,'<sup>$1</sup>')}\nfunction esc(t){", 1)
js = js.replace("$('#q').oninput=function(){renderTOC(this.value)};", r"""$('#q').oninput=function(){renderTOC(this.value)};
$('#q').onkeydown=function(e){if(e.key==='Enter'){e.preventDefault();search(this.value)}};
/* full-text search: Enter in the box lists matching paragraphs */
function search(q){
  q=(q||'').trim(); if(q.length<3)return; stop();
  var lq=q.toLowerCase(), hits=[];
  BOOK.papers.forEach(function(p){p.sections.forEach(function(s){s.paras.forEach(function(x){
    if(hits.length<300&&x.text.toLowerCase().indexOf(lq)>=0)hits.push(x)})})});
  var re=new RegExp(q.replace(/[.*+?^${}()|[\]\\]/g,'\\$&'),'gi');
  var h='<h2 class="pt">Search: '+esc(q)+'</h2><div class="pn">'+(hits.length>=300?'300+':hits.length)+' PARAGRAPHS</div>';
  hits.forEach(function(x){h+='<div class="res" data-r="'+x.cit+'"><b>'+x.cit+'</b> &nbsp;'+fmt(x.text).replace(re,function(m){return '<mark>'+m+'</mark>'})+'</div>'});
  $('#wrap').innerHTML=h;window.scrollTo(0,0);
  if(window.innerWidth<=900)$('#side').classList.remove('open');
}
$('#wrap').addEventListener('click',function(e){var r=e.target.closest('.res');if(r){location.hash=r.dataset.r}});""")
head = '''<!doctype html>
<html lang="en"><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>The Urantia Book — Online</title>
<meta name="description" content="Read The Urantia Book online: contents, paper and section navigation, full-text search, and read-aloud.">
''' + css + '''
</head><body>
<header>
 <button class="btn" id="burger">☰ Contents</button>
 <h1>The Urantia Book <span style="opacity:.6;font-weight:400">Online</span></h1>
 <span class="sp"></span>
 <div class="play">
   <select id="scope" title="How far to read">
     <option value="ch">This section</option>
     <option value="pa">Whole paper</option>
     <option value="all">Keep going</option>
   </select>
   <button id="playch" class="g">▶ Listen</button>
   <button id="stop">■ Stop</button>
 </div>
 <select id="voice" title="Voice"></select>
 <input type="range" id="rate" min="0.6" max="1.3" step="0.05" value="0.9" title="Speed" style="width:86px">
 <button class="btn" id="wide" title="Text width">↔</button>
 <button class="btn" id="fs" title="Font size">A</button>
 <button class="btn" id="dark" title="Dark mode">◐</button>
 <button class="btn" id="home" title="Resources home">⌂</button>
</header>
<main>
 <aside id="side">
   <input id="q" placeholder="Find a paper · Enter = search the text">
   <div id="toc"></div>
 </aside>
 <section id="body"><div class="wrap" id="wrap"><p style="color:var(--dim)">Loading…</p></div></section>
</main>
'''
out = head + js
left = re.findall(r'.{25}[가-힣]+.{10}', out)
assert not left, left[:5]
open(r'E:/OneDrive/문서/GitHub/uui-resources/book/index.html', 'w', encoding='utf-8').write(out)
print('ok', len(out))
