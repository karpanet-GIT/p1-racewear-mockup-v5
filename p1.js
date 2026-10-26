(function(){
var D=document;
function DCLogic(props){this.props=props||{};this.state={};}
DCLogic.prototype.setState=function(p){Object.assign(this.state,typeof p==='function'?p(this.state):p);render();};
DCLogic.prototype.renderVals=function(){return {};};
window.DCLogic=DCLogic;
var DEF={topbar:'100% fatto a mano in Italia \u00b7 Omologazione FIA 8856-2018 \u00b7 Su misura e personalizzazione',b2bLink:'Area B2B team e rivenditori'};
var HOLE=/\{\{([^}]+)\}\}/g, ONE=/^\{\{([^}]+)\}\}$/;
function get(s,p){p=p.trim();if(p==='true')return true;if(p==='false')return false;var a=p.split('.'),v=s;for(var i=0;i<a.length;i++){if(v==null)return undefined;v=v[a[i]];}return v;}
function interp(t,s){return t.replace(HOLE,function(m,p){var v=get(s,p);return v==null?'':String(v);});}
function kids(n){return n.tagName&&n.tagName.toLowerCase()==='template'?n.content.childNodes:n.childNodes;}
function nodes(list,s,parent){for(var i=0;i<list.length;i++)node(list[i],s,parent);}
function node(n,s,parent){
if(n.nodeType===3){parent.appendChild(D.createTextNode(interp(n.nodeValue,s)));return;}
if(n.nodeType!==1)return;
var sc=n.getAttribute('data-sc');
if(sc==='for'){var m=(n.getAttribute('list')||'').match(ONE),l=m?get(s,m[1]):[],as=n.getAttribute('as')||'item';(l||[]).forEach(function(it,i){var c=Object.create(s);c[as]=it;c.$index=i;nodes(kids(n),c,parent);});return;}
if(sc==='if'){var e=n.getAttribute('value')||'',m2=e.match(ONE),v=m2?get(s,m2[1]):e;if(v)nodes(kids(n),s,parent);return;}
if(n.localName==='helmet')return;
var el=n.namespaceURI==='http://www.w3.org/1999/xhtml'?D.createElement(n.localName):D.createElementNS(n.namespaceURI,n.localName);
for(var j=0;j<n.attributes.length;j++){var at=n.attributes[j],nm=at.name,val=at.value,mm=val.match(ONE);
if(mm){var x=get(s,mm[1]);
if(/^on/.test(nm)){if(typeof x==='function')el.addEventListener(nm.slice(2),x);continue;}
if(nm==='checked'||nm==='disabled'||nm==='selected'){if(x===true||x==='true')el.setAttribute(nm,'');continue;}
if(x==null||x===false)continue;el.setAttribute(nm,String(x));}
else el.setAttribute(nm,interp(val,s));}
nodes(n.childNodes,s,el);
if(n.localName==='input'&&el.hasAttribute('checked'))el.checked=true;
parent.appendChild(el);}
var tpl,comp,app,page=D.body.getAttribute('data-page'),props={},hasCanale=false;
function render(){var vals=comp.renderVals(),s=Object.assign({},DEF,vals),f=D.createDocumentFragment(),y=window.scrollY;nodes(tpl.content.childNodes,s,f);app.replaceChildren(f);
var cur=app.querySelector('[data-nav="'+page+'"]');if(cur)cur.style.borderBottom='2px solid #DBFB00';
window.scrollTo(0,y);bar();}
function bar(){var b=D.getElementById('p1bar');if(!b){b=D.createElement('nav');b.id='p1bar';b.setAttribute('aria-label','Navigazione mockup');D.body.appendChild(b);}
var P=[['home','/','Homepage'],['storia','/storia','Storia'],['categoria','/categoria','Categoria'],['prodotto','/prodotto','Prodotto']];
var h='<span class="p1l">MOCKUP</span>'+P.map(function(p){return '<a href="'+p[1]+'"'+(p[0]===page?' aria-current="page"':'')+'>'+p[2]+'</a>';}).join('');
if(hasCanale){var c=props.canale||'B2C';h+='<span class="p1sep"></span><button type="button" data-c="B2C" aria-pressed="'+(c==='B2C')+'">B2C</button><button type="button" data-c="B2B" aria-pressed="'+(c==='B2B')+'">B2B</button>';}
b.innerHTML=h;b.querySelectorAll('button').forEach(function(x){x.onclick=function(){props.canale=x.getAttribute('data-c');comp.props=props;render();};});}
function start(){Promise.all([fetch('/top.txt').then(function(r){return r.text();}),fetch('/bottom.txt').then(function(r){return r.text();})]).then(function(t){go(t[0],t[1]);});}
var IMG={IQBU3ock:'/img/hero.avif',IQDNI14I:'/img/fuoco.webp',IQA0FRJj:'/img/team.webp',IQC5DKsw:'/img/enrico.avif'};
function fixImg(src){
src=src.replace(/https:\/\/ntsproject-my\.sharepoint\.com\/[^"]*?(IQBU3ock|IQDNI14I|IQA0FRJj|IQC5DKsw)[^"]*/g,function(m,k){return IMG[k];});
return src.replace(/<img\b[^>]*ntsproject-my\.sharepoint\.com[^>]*>/g,'');}
function go(TOP,BOT){
var src=D.getElementById('tpl').textContent;
src=src.replace('<!--TOP-->',TOP).replace('<!--BOTTOM-->',BOT);
src=fixImg(src);
src=src.replace(/<sc-(for|if)\b/g,'<template data-sc="$1"').replace(/<\/sc-(for|if)>/g,'</template>');
src=src.replace(/(href=")(Main|Storia|Categoria|Prodotto)\.dc\.html/g,function(m,a,b){return a+({Main:'/',Storia:'/storia',Categoria:'/categoria',Prodotto:'/prodotto'})[b];});
tpl=D.createElement('template');tpl.innerHTML=src;
var hm=tpl.content.querySelector('helmet');if(hm){Array.prototype.forEach.call(hm.children,function(c){D.head.appendChild(c.cloneNode(true));});}
var ls=D.getElementById('logic'),pd={};try{pd=JSON.parse(ls.getAttribute('data-props')||'{}');}catch(e){}
Object.keys(pd).forEach(function(k){if(k.charAt(0)!=='$'&&pd[k]&&'default' in pd[k])props[k]=pd[k]['default'];});
hasCanale='canale' in props;var q=new URLSearchParams(location.search).get('canale');if(q&&hasCanale)props.canale=q;
var C=new Function('DCLogic',ls.textContent+'\nreturn Component;')(DCLogic);
app=D.getElementById('app');comp=new C(props);if(!comp.state)comp.state={};
render();if(location.hash){var t=D.getElementById(location.hash.slice(1));if(t)t.scrollIntoView();}}
if(D.readyState==='loading')D.addEventListener('DOMContentLoaded',start);else start();
})();
