(function(){
'use strict';
var S=window.SITE||{};
var reduce=window.matchMedia&&matchMedia('(prefers-reduced-motion:reduce)').matches;
var $=function(s,r){return (r||document).querySelector(s)};
var $$=function(s,r){return Array.prototype.slice.call((r||document).querySelectorAll(s))};

/* 1. transition between pages: main fades out, then the link opens */
if(!reduce){
  document.addEventListener('click',function(e){
    var a=e.target.closest&&e.target.closest('a[href]');
    if(!a||e.defaultPrevented||e.button!==0||e.metaKey||e.ctrlKey||e.shiftKey||e.altKey)return;
    if(a.target&&a.target!=='_self'||a.hasAttribute('download'))return;
    var u=new URL(a.href,location.href);
    if(u.origin!==location.origin||u.pathname===location.pathname&&u.search===location.search)return;
    if(!/\.html$|\/$/.test(u.pathname))return;
    e.preventDefault();
    var m=$('main');if(m)m.classList.add('leaving');
    setTimeout(function(){location.href=a.href},450);
  });
  window.addEventListener('pageshow',function(e){if(e.persisted){var m=$('main');if(m)m.classList.remove('leaving')}});
}

/* 2. photo bands: lazy loading, shimmer first, then the photo fades in */
function loadBand(el){
  var bg=document.createElement('div');bg.className='bgimg';el.insertBefore(bg,el.firstChild);
  var im=new Image();
  im.onload=function(){
    bg.style.backgroundImage='url('+im.src+')';
    bg.style.backgroundPosition=el.getAttribute('data-pos')||'center';
    setTimeout(function(){bg.classList.add('loaded')},reduce?0:900);
  };
  im.src=el.getAttribute('data-bg');
}
var bands=$$('.bgband[data-bg]');
if('IntersectionObserver' in window){
  var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){loadBand(e.target);io.unobserve(e.target)}})},{rootMargin:'120px'});
  bands.forEach(function(b){io.observe(b)});
}else bands.forEach(loadBand);

/* 3. cards come in one after the other while scrolling */
if(!reduce){
  var rv=$$('.three .v,.grid .card,.bigmap,main form,details.faq');
  rv.forEach(function(el){var i=Array.prototype.indexOf.call(el.parentNode.children,el);el.style.setProperty('--d',Math.min(i,5)*0.12+'s');el.classList.add('rv')});
  if('IntersectionObserver' in window){
    var io2=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io2.unobserve(e.target)}})},{threshold:.12});
    rv.forEach(function(el){io2.observe(el)});
    setTimeout(function(){rv.forEach(function(el){el.classList.add('in')})},4000);
  }else rv.forEach(function(el){el.classList.add('in')});
}

/* 4. schematic map of Crete */
var CRETE=[[23.53,35.27],[23.57,35.40],[23.58,35.58],[23.66,35.60],[23.78,35.57],[23.80,35.52],[24.02,35.52],[24.10,35.58],[24.22,35.52],[24.20,35.45],[24.25,35.37],[24.48,35.37],[24.78,35.42],[24.96,35.39],[25.13,35.34],[25.38,35.32],[25.46,35.29],[25.60,35.25],[25.72,35.19],[25.73,35.26],[25.77,35.27],[25.95,35.21],[26.10,35.22],[26.27,35.25],[26.32,35.31],[26.30,35.20],[26.25,35.10],[25.74,35.00],[25.50,34.99],[25.20,34.95],[24.90,34.93],[24.75,34.93],[24.75,34.99],[24.69,35.10],[24.45,35.17],[24.18,35.20],[24.07,35.20],[23.96,35.23],[23.80,35.24],[23.68,35.23],[23.55,35.25]];
var PTS={chq:[24.15,35.53,'a'],her:[25.18,35.34,'a'],port:[25.14,35.35,'p'],cha:[24.02,35.51,'t'],ret:[24.48,35.37,'t'],hei:[25.10,35.33,'t'],agn:[25.72,35.19,'t'],sit:[26.10,35.21,'t'],che:[25.38,35.32,'t']};
function esc(t){return String(t).replace(/&/g,'&amp;').replace(/</g,'&lt;')}
function bigMap(from,to){
  var Sc=190,k=0.816;
  function X(lon){return 10+(lon-23.45)*k*Sc}
  function Y(lat){return 10+(35.66-lat)*Sc}
  var land=CRETE.map(function(c,i){return (i?'L':'M')+X(c[0]).toFixed(1)+' '+Y(c[1]).toFixed(1)}).join(' ')+'Z';
  var show=['cha','ret','hei','agn','sit','chq','her'],dots='',lbl='',path='',id;
  for(id in PTS){
    var p=PTS[id],x=X(p[0]),y=Y(p[1]),sel=id===from||id===to;
    dots+='<circle class="'+(sel?'sel':p[2]==='a'?'air':'town')+'" cx="'+x.toFixed(1)+'" cy="'+y.toFixed(1)+'" r="'+(sel?7:p[2]==='a'?5:4)+'"/>';
    if(sel||(show.indexOf(id)>-1&&p[2]==='t')){
      var up=id==='cha'||id==='ret'||id==='sit'||id==='hei';
      lbl+='<text x="'+x.toFixed(1)+'" y="'+(y+(up?-12:20)).toFixed(1)+'" text-anchor="middle">'+esc(S.pts[id])+'</text>';
    }
  }
  if(from&&to&&from!==to){var a=PTS[from],b=PTS[to];path='<path class="path" d="M'+X(a[0]).toFixed(1)+' '+Y(a[1]).toFixed(1)+' L'+X(b[0]).toFixed(1)+' '+Y(b[1]).toFixed(1)+'"/>'}
  return '<svg viewBox="0 0 480 175" role="img" aria-label="'+esc(S.mapLabel)+'"><path class="land" d="'+land+'"/>'+path+dots+lbl+'</svg>'+
    '<div class="legend"><span><i class="a"></i>'+esc(S.lg[0])+'</span><span><i class="t"></i>'+esc(S.lg[1])+'</span><span><i class="b"></i>'+esc(S.lg[2])+'</span><span>· '+esc(S.mapnote)+'</span></div>';
}
var maps=$$('[data-map]');
if(maps.length&&S.pts){
  var f=$('#bfrom'),t=$('#bto');
  function draw(){maps.forEach(function(m){m.innerHTML=bigMap(f?f.value:null,t?t.value:null)})}
  var q=new URLSearchParams(location.search);
  if(f&&t){
    if(q.get('from')&&PTS[q.get('from')])f.value=q.get('from');
    if(q.get('to')&&PTS[q.get('to')])t.value=q.get('to');
    f.addEventListener('change',draw);t.addEventListener('change',draw);
  }
  draw();
}

/* 5. booking form: no sending yet, the endpoint is empty until the database is connected */
var bf=$('#bf');
if(bf){
  bf.addEventListener('submit',function(e){
    e.preventDefault();
    if($('#bhp').value)return;
    if(!bf.checkValidity()){bf.reportValidity();return}
    var ok=$('#bok');ok.hidden=false;
    if(S.formEndpoint){/* later: fetch(S.formEndpoint,{method:'POST',body:new FormData(bf)}) */}
  });
}

/* 6. chat with keyword answers */
if(S.chat){
  var C=S.chat,hist=[];
  var btn=document.createElement('button');btn.id='chatBtn';btn.type='button';btn.textContent=C.title;btn.setAttribute('aria-expanded','false');btn.setAttribute('aria-controls','chat');
  var box=document.createElement('aside');box.id='chat';box.hidden=true;box.setAttribute('aria-label',C.title);
  box.innerHTML='<header><span>'+esc(C.title)+'</span><button type="button" id="chatX" aria-label="Close">×</button></header><div id="log" aria-live="polite"></div><div class="quick" id="quick"></div><form id="chatForm"><input id="chatIn" autocomplete="off" aria-label="'+esc(C.input)+'" placeholder="'+esc(C.input)+'"><button type="submit">'+esc(C.send)+'</button></form>';
  document.body.appendChild(btn);document.body.appendChild(box);
  var log=$('#log',box);
  function add(r,x,link){
    var d=document.createElement('div');d.className='msg '+r;d.textContent=x;
    if(link){var a=document.createElement('a');a.href=link[0];a.textContent=' → '+link[1];d.appendChild(a)}
    log.appendChild(d);log.scrollTop=1e6;
  }
  add('bot',C.hi);
  var pageFile={book:'book.html',routes:'routes.html',contact:'contact.html',home:'index.html'};
  function say(key,label){
    var b=C.bot[key]||C.bot.def;
    add('bot',b[0],[pageFile[b[1]],C.nav[b[1]]]);
  }
  $('#quick',box).innerHTML=C.quick.map(function(q){return '<button type="button" data-q="'+q[1]+'">'+esc(q[0])+'</button>'}).join('');
  $('#quick',box).addEventListener('click',function(e){var b=e.target.closest('button');if(!b)return;add('me',b.textContent);say(b.getAttribute('data-q')==='routes'?'air':b.getAttribute('data-q'))});
  $('#chatForm',box).addEventListener('submit',function(e){
    e.preventDefault();var inp=$('#chatIn',box),v=inp.value.trim();if(!v)return;inp.value='';add('me',v);
    var key='def';for(var k in C.kw){if(new RegExp(C.kw[k],'i').test(v)){key=k;break}}
    say(key);
  });
  btn.addEventListener('click',function(){box.hidden=!box.hidden;btn.setAttribute('aria-expanded',String(!box.hidden));if(!box.hidden)$('#chatIn',box).focus()});
  $('#chatX',box).addEventListener('click',function(){box.hidden=true;btn.setAttribute('aria-expanded','false')});
}
})();
