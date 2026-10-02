import openpyxl, json, re, html
ws = openpyxl.load_workbook(r'E:/OneDrive/내 문서/유란시아/용어집/English_Master_Glossary.xlsx', read_only=True)['English_Master_Glossary']
rows = []
for a, b in ws.iter_rows(min_row=2, values_only=True):
    a = re.sub(r'\s+', ' ', str(a or '')).strip(); b = re.sub(r'\s+', ' ', str(b or '')).strip()
    if a and b: rows.append([a, b])
seen = set(); data = []
for a, b in sorted(rows, key=lambda r: r[0].lower()):
    k = (a.lower(), b)
    if k in seen: continue
    seen.add(k); data.append(r := [a, b])
letters = sorted({r[0][0].upper() for r in data if r[0][0].isalpha()})
page = '''<!doctype html>
<html lang="en"><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Urantia Book Glossary</title>
<meta name="description" content="A glossary of Urantia Book terms, names, and places — search or browse A to Z.">
<style>
:root{--navy:#0f2244;--gold:#c9a227;--bg:#f7f5f0;--card:#fff;--ink:#20242c;--dim:#6b7280;--line:#e3ded3}
@media (prefers-color-scheme:dark){:root{--bg:#12141a;--card:#181b22;--ink:#dfe3ea;--dim:#98a0ae;--line:#2b3040}}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font-family:Georgia,"Times New Roman",serif}
header{background:linear-gradient(180deg,#132a55,#0d1c3a);border-bottom:3px solid var(--gold);color:#fff;position:sticky;top:0;z-index:5}
.top{max-width:980px;margin:0 auto;padding:12px 16px 8px;display:flex;gap:12px;align-items:center;flex-wrap:wrap}
.top h1{margin:0;font-size:19px;font-weight:600;flex:1;min-width:180px}
.top a{color:#fff;text-decoration:none;font-size:13px;border:1px solid rgba(255,255,255,.3);border-radius:999px;padding:5px 12px}
#q{flex:1 1 260px;font:inherit;font-size:15px;padding:8px 12px;border-radius:9px;border:1px solid rgba(255,255,255,.3);background:rgba(255,255,255,.1);color:#fff}
#q::placeholder{color:rgba(255,255,255,.6)}
.az{max-width:980px;margin:0 auto;padding:0 12px 10px;display:flex;flex-wrap:wrap;gap:3px}
.az a{color:#fff;text-decoration:none;font-size:13.5px;font-weight:700;min-width:28px;text-align:center;padding:4px 0;border-radius:6px}
.az a:hover{background:var(--gold);color:#15203a}
.az a.off{opacity:.3;pointer-events:none}
main{max-width:980px;margin:0 auto;padding:16px 16px 80px}
.count{color:var(--dim);font-size:13.5px;margin:4px 0 14px}
h2{font-size:30px;color:var(--gold);margin:28px 0 8px;border-bottom:1px solid var(--line);padding-bottom:4px;scroll-margin-top:120px}
dl{margin:0}
.e{display:flex;gap:18px;padding:10px 4px;border-bottom:1px solid var(--line)}
dt{flex:0 0 240px;font-weight:700;color:var(--navy);font-size:16px}
@media (prefers-color-scheme:dark){dt{color:#cfe0ff}}
dd{margin:0;flex:1;line-height:1.65;font-size:15.5px}
mark{background:rgba(201,162,39,.35);color:inherit}
.none{color:var(--dim);padding:30px 0;text-align:center}
.src{color:var(--dim);font-size:12.5px;margin-top:40px;line-height:1.6}
@media(max-width:640px){.e{display:block}dt{margin-bottom:3px}.top h1{font-size:17px}}
</style>
</head><body>
<header>
 <div class="top"><h1>Urantia Book Glossary</h1><input id="q" type="search" placeholder="Search terms and definitions" autocomplete="off"><a href="../">⌂ Resources</a></div>
 <nav class="az" id="az"></nav>
</header>
<main>
 <div class="count" id="count"></div>
 <div id="list"></div>
 <p class="src">Glossary entries: English Master Glossary of The Urantia Book (volunteer edition). Arranged for alphabetical browsing.</p>
</main>
<script>
var G=__DATA__;
var $=function(i){return document.getElementById(i)};
function esc(t){return t.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;')}
function letter(t){var c=t.charAt(0).toUpperCase();return /[A-Z]/.test(c)?c:'#'}
var ALL='ABCDEFGHIJKLMNOPQRSTUVWXYZ'.split('');
function render(q){
  q=(q||'').trim().toLowerCase();
  var re=q?new RegExp(q.replace(/[.*+?^${}()|[\\]\\\\]/g,'\\\\$&'),'gi'):null;
  var hl=function(t){t=esc(t);return re?t.replace(re,function(m){return '<mark>'+m+'</mark>'}):t};
  var rows=q?G.filter(function(r){return r[0].toLowerCase().indexOf(q)>=0||r[1].toLowerCase().indexOf(q)>=0}):G;
  if(q)rows=rows.slice().sort(function(a,b){return (b[0].toLowerCase().indexOf(q)>=0)-(a[0].toLowerCase().indexOf(q)>=0)});
  var h='',cur='',have={};
  rows.forEach(function(r){var L=letter(r[0]);have[L]=1;
    if(!q&&L!==cur){if(cur)h+='</dl>';h+='<h2 id="L'+L+'">'+L+'</h2><dl>';cur=L}
    h+='<div class="e"><dt>'+hl(r[0])+'</dt><dd>'+hl(r[1])+'</dd></div>'});
  if(q)h='<dl>'+h+'</dl>'; else if(cur)h+='</dl>';
  $('list').innerHTML=rows.length?h:'<div class="none">No entries found.</div>';
  $('count').textContent=q?rows.length+' of '+G.length+' entries':G.length+' entries';
  $('az').innerHTML=ALL.map(function(L){return '<a href="#L'+L+'"'+(have[L]||q?'':' class="off"')+' data-l="'+L+'">'+L+'</a>'}).join('');
}
$('q').oninput=function(){render(this.value)};
$('az').onclick=function(e){var a=e.target.closest('a');if(!a)return;if($('q').value){e.preventDefault();$('q').value='';render('');location.hash='L'+a.dataset.l}};
render('');
</script>
</body></html>
'''
page = page.replace('__DATA__', json.dumps(data, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/'))
import os
os.makedirs(r'E:/OneDrive/문서/GitHub/uui-resources/glossary', exist_ok=True)
open(r'E:/OneDrive/문서/GitHub/uui-resources/glossary/index.html', 'w', encoding='utf-8').write(page)
print(len(data), letters, len(page))
