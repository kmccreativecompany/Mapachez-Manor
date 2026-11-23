// Offline state-machine and real manor-pathfinding checks. No browser or packages required.
// Run: node --test tests/test_tea.mjs
import {readFileSync} from 'node:fs';
import vm from 'node:vm';
import test from 'node:test';
import assert from 'node:assert/strict';

const html=readFileSync(new URL('../index.html',import.meta.url),'utf8');
const module=html.split('/* ==== CONSERVATORY TEA v1:')[1].split('/* ==== end CONSERVATORY TEA v1 ==== */')[0];
const source='/* CONSERVATORY TEA v1:'+module;
const geometry=html.slice(html.indexOf('const W=1280'),html.indexOf('function rect(c,'));
const manorClass=html.match(/class ManorWorld \{[\s\S]*?\n\}\n/)[0];

function harness(saved){
 const context=vm.createContext({console,structuredClone});
 vm.runInContext(`
 let state=${JSON.stringify(saved||{seed:44,phase:'playing',minute:7,player:{x:260,y:650},flags:{briefed:true},metrics:{trust:72,care:72,team:72},sideStories:{fern:true},inventory:['a tray']})};
 let festivalActive=false,titleVisible=false,profile={lang:'en'},narrativeText='',options=[],markup='',saves=0;
 const body={innerText:'',querySelectorAll:()=>[],querySelector:()=>({}),append:()=>{}};
 const places={onclick:()=>{}};
 const $=()=>places;
 const document={createElement:()=>({}),head:{append:()=>{}}};
 const mixDefault=()=>({kind:'human'}),mixRecipe=(v,color)=>({...v,color,kind:'human'});
 const esc=x=>String(x).replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('>','&gt;');
 const save=()=>{saves++;};
 const openModal=h=>{markup=h;body.innerText=h;};
 const titleHTML=(t,k)=>'<h2>'+t+'</h2><small>'+k+'</small>';
 const choices=o=>{options=o;},closeModal=()=>{},paintBust=()=>{};
 let interact=id=>'original:'+id,conservatory=()=>{};
 ${geometry}
 ${manorClass}
 const world=Object.create(ManorWorld.prototype);
 Object.assign(world,{keys:new Set(),path:[],options:{state:()=>state,festival:()=>festivalActive,extras:()=>[],drawExtras:()=>{}},stop:()=>{}});
 `,context);
 vm.runInContext(source,context);
 return {
  context,
  run:s=>vm.runInContext(s,context),
  value:s=>JSON.parse(JSON.stringify(vm.runInContext(s,context))),
  click:text=>vm.runInContext(`options.find(o=>o.text===${JSON.stringify(text)}).run()`,context)
 };
}

test('all inline JavaScript compiles',()=>{
 let count=0;
 for(const [,attrs,code] of html.matchAll(/<script\b([^>]*)>([\s\S]*?)<\/script>/gi)){
  if(/type=["']application\//.test(attrs))continue;
  new vm.Script(code);count++;
 }
 assert.ok(count>0);
});

test('the opening conceals the connection and partial reading resumes exactly',()=>{
 const h=harness();h.run('openTeaConversation()');
 assert.match(h.value('markup'),/husband can&#39;t|husband can't/);
 assert.doesNotMatch(h.value('markup'),/divorce|boyfriend|invoice|settlement/i);
 h.click('Keep listening');
 const progress=h.value('state.sideStories.tea');
 assert.equal(progress.lines,6);assert.equal(progress.beat,0);
 const resumed=harness(h.value('state'));resumed.run('openTeaConversation()');
 assert.deepEqual(resumed.value('state.sideStories.tea'),progress);
 assert.match(resumed.value('markup'),/Location sharing is off/);
 assert.equal(resumed.value('state.sideStories.fern'),true);
});

test('five scenes reveal in order; replay never loses progress or changes hotel scores',()=>{
 const h=harness(),before=h.value('state');h.run('openTeaConversation()');
 for(let beat=0;beat<5;beat++){
  while(h.run("options.some(o=>o.text==='Keep listening')"))h.click('Keep listening');
  assert.equal(h.value('teaProgress().beat'),beat);
  if(beat===0)assert.doesNotMatch(h.value('markup'),/divorce|boyfriend/i);
  if(beat===1)assert.match(h.value('markup'),/divorce lawyer[\s\S]*boyfriend/);
  if(beat===2)assert.match(h.value('markup'),/larger your fee/);
  if(beat===3)assert.match(h.value('markup'),/Which table/);
  if(beat<4)h.click('Listen a little longer');
 }
 assert.match(h.value('markup'),/I hired him to find out if you were leaving me/);
 assert.match(h.value('markup'),/To be continued/);
 const completed=h.value('teaProgress()');assert.equal(completed.finished,true);
 const after=h.value('state');
 for(const key of ['minute','metrics','flags','inventory','player'])assert.deepEqual(after[key],before[key],key);
 h.click('Hear the conversation again');h.click('Keep listening');
 assert.deepEqual(h.value('teaProgress()'),completed);
 const resumed=harness(after);resumed.run('openTeaConversation()');
 assert.equal(resumed.value('teaProgress().finished'),true);
 assert.match(resumed.value('markup'),/To be continued/);
});

test('old or malformed side-story saves are safe and cannot mark an unseen ending complete',()=>{
 const h=harness();
 for(const value of [null,[],true,'broken',{beat:NaN},{beat:Infinity},{beat:-1,lines:-1,finished:true},{beat:0,lines:999,finished:true}]){
  const normalized=h.value(`normaliseTeaProgress(${JSON.stringify(value)})`);
  assert.equal(normalized.finished,false);
  assert.ok(normalized.beat>=0&&normalized.beat<5);
 }
 h.run('state.sideStories=[];openTeaConversation()');
 assert.equal(h.value('state.sideStories.tea.version'),1);
 h.run('festivalActive=true');const saved=h.value('saves');h.run('openTeaConversation()');
 assert.equal(h.value('saves'),saved);
 h.run("festivalActive=false;state.phase='ended';openTeaConversation()");
 assert.equal(h.value('saves'),saved);
});

test('chairs and table block walking while tea, piano and alternate doorway stay reachable',()=>{
 const h=harness();
 for(const point of [[920,550],[970,548],[1020,550],[976,608]])assert.equal(h.run(`world.walkable(${point})`),false);
 for(const [x,y] of [[944,608],[1042,624],[699,505]]){
  const path=h.value(`world.route(${x},${y})`);assert.ok(path.length,`No route to ${x},${y}`);
  assert.ok(h.run(`world.walkable(${path.at(-1).x},${path.at(-1).y})`));
 }
 h.run("state.flags.hazard='secured'");
 assert.ok(h.value('world.route(TEA_SPOT.x,TEA_SPOT.y)').length,'Alternate entrance must work');
 assert.equal(h.run("interact('desk')"),'original:desk');
 assert.equal(h.run("world.options.extras().filter(p=>p.id==='conservatory-tea').length"),1);
});

test('English and Spanish keep the same reveals and story controls',()=>{
 const h=harness(),en=h.value('TEA_SCENES.en'),es=h.value('TEA_SCENES.es');
 assert.equal(en.length,es.length);
 for(let i=0;i<en.length;i++)assert.deepEqual(en[i].lines.map(l=>l[0]),es[i].lines.map(l=>l[0]));
 h.run("profile.lang='es';openTeaConversation()");
 assert.match(h.value('markup'),/Mi marido no puede saber/);
 h.click('Seguir escuchando');assert.equal(h.value('teaProgress().lines'),6);
 assert.doesNotMatch(JSON.stringify(en),/\bsex\b|slept|bedroom|undress|naked/i);
 assert.doesNotMatch(JSON.stringify(en),/Adrian|Mrs\. Vale/);
 assert.equal(h.run('TEA_PEOPLE.wife.recipe.kind'),h.run('TEA_PEOPLE.husband.recipe.kind'));
});

test('a tabletop tap uses the clear interaction spot and is ignored while a dialog is open',()=>{
 const h=harness();
 h.run(`let tapped=null,paused=false;
  Object.assign(world,{canvas:{getBoundingClientRect:()=>({left:0,top:0})},ox:0,oy:0,scale:1,go:id=>{tapped=id;}});
  world.options.active=()=>true;world.options.paused=()=>paused;
  world.pointer({clientX:970,clientY:548});`);
 assert.equal(h.value('tapped'),'conservatory-tea');
 assert.equal(h.run('world.walkable(TEA_SPOT.x,TEA_SPOT.y)'),true);
 h.run('tapped=null;paused=true;world.pointer({clientX:970,clientY:548})');
 assert.equal(h.value('tapped'),null);
});
