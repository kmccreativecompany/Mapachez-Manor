/* Pixel art source. Inlined into the offline game by the render integration. */
function pixelPaint(c,r,dir='down',phase=0,blink=false,carrying=false){
  const ink='#302431',gold='#d4a85d',shine='#ffe0a0',cream='#f4dfbc';
  const shade=(s,f)=>{const n=parseInt(String(s||'#987961').slice(1,7),16)||0,t=f<0?0:255,p=Math.abs(f),m=v=>Math.round(v+(t-v)*p);return '#'+((1<<24)|(m(n>>16)<<16)|(m(n>>8&255)<<8)|m(n&255)).toString(16).slice(1)};
  const skin=r.skin||'#eac19b',hair=r.hair||'#5d3b32',coat=r.color||'#386650',skD=shade(skin,-.28),skL=shade(skin,.26),hD=shade(hair,-.42),hM=shade(hair,.22),hL=shade(hair,.42),coD=shade(coat,-.42),coL=shade(coat,.28);
  const rac=r.kind==='raccoon',robot=r.kind==='construct',folk=r.kind==='human'||r.kind==='fae',fae=r.kind==='fae',monster=r.kind==='monster',alien=r.kind==='alien',back=dir==='up',dx=dir==='left'?-3:dir==='right'?3:0,side=dx!==0,ex=new Set([r.extra,r.extra2]),has=x=>ex.has(x),seed=Math.floor(r.seed||0),hd=r.hairdo||'short';
  const R=(x,y,w,h,col)=>{c.fillStyle=col;c.fillRect(Math.round(x),Math.round(y),Math.max(0,Math.round(w)),Math.max(0,Math.round(h)));};
  // Integer scanlines: the image contains intentional pixels, never antialiased curves.
  const P=(pts,col)=>{let lo=Math.max(0,Math.floor(Math.min(...pts.map(v=>v[1])))),hi=Math.min(64,Math.ceil(Math.max(...pts.map(v=>v[1]))));c.fillStyle=col;for(let y=lo;y<hi;y++){let xs=[];for(let i=0,j=pts.length-1;i<pts.length;j=i++){const [a,b]=pts[i],[d,e]=pts[j];if((b>y+.5)!==(e>y+.5))xs.push(a+(y+.5-b)*(d-a)/(e-b));}xs.sort((a,b)=>a-b);for(let i=0;i+1<xs.length;i+=2){const a=Math.ceil(xs[i]-.5),b=Math.ceil(xs[i+1]-.5);if(b>a)c.fillRect(a,y,b-a,1);}}};
  const B=(x,y,w,h,col,edge=ink)=>{P([[x+3,y],[x+w-3,y],[x+w,y+3],[x+w,y+h-3],[x+w-3,y+h],[x+3,y+h],[x,y+h-3],[x,y+3]],edge);P([[x+4,y+1],[x+w-4,y+1],[x+w-1,y+4],[x+w-1,y+h-4],[x+w-4,y+h-1],[x+4,y+h-1],[x+1,y+h-4],[x+1,y+4]],col)};
  const dot=(x,y,col=gold)=>R(x,y,2,2,col);
  const eye=(x,y,w=5,h=7,iris='#694b42')=>{if(blink){R(x,y+3,w,1,ink);R(x+1,y+4,Math.max(1,w-2),1,ink);return}R(x+1,y-1,w-1,1,ink);R(x,y,w,h-1,ink);R(x+1,y+h-1,w-2,1,ink);R(x+1,y+1,w-2,h-3,'#fff2dc');const u=x+Math.max(1,Math.min(w-3,2+(dx>0?1:dx<0?-1:0)));R(u,y+1,Math.min(3,w-2),h-2,shade(iris,-.25));R(u,y+3,Math.min(3,w-2),h-4,iris);R(u,y+1,1,2,'#fff9e8');if(w>=5)R(u+1,y+h-3,1,1,shade(iris,.48));};
  const leaf=(x,y,k=1)=>{P([[x,y],[x+4*k,y-4],[x+6*k,y-4],[x+5*k,y],[x+2*k,y+2]],'#587c48');R(x,y,2,1,'#a7b96a')};
  const flower=(x,y)=>{R(x+1,y,2,4,'#eac3af');R(x,y+1,4,2,'#f4b7aa');R(x+1,y+1,2,2,shine)};
  const hx=24+dx,cy=folk||rac||robot?24:r.body==='tall'?22:r.body==='blob'?30:25,headTop=cy-13,headBottom=cy+12,headW=rac?30:robot?26:folk?26:r.body==='round'?32:r.body==='blob'?32:25,hl=hx-Math.floor(headW/2),hr=hl+headW;
  // Ground contact is fixed; the walk pose only changes the individual feet.
  P([[9,54],[13,52],[35,52],[39,54],[35,57],[13,57]],'#20392e44');
  if(has('glow'))P([[hx-18,cy-10],[hx-12,cy-18],[hx+12,cy-18],[hx+18,cy-10],[hx+18,cy+14],[hx+12,cy+20],[hx-12,cy+20],[hx-18,cy+14]],'#a7dfda38');
  if(has('wings')&&fae){for(const k of [-1,1]){P([[24,35],[24+k*5,27],[24+k*11,22],[24+k*19,23],[24+k*20,30],[24+k*15,36],[24+k*8,38],[24+k*15,43],[24+k*12,46],[24+k*4,42]],ink);P([[24+k*3,35],[24+k*10,25],[24+k*17,24],[24+k*18,29],[24+k*13,34],[24+k*6,37],[24+k*13,42],[24+k*12,44],[24+k*5,41]],'#9cbdc7');P([[24+k*5,35],[24+k*10,27],[24+k*16,25],[24+k*14,31],[24+k*9,34]],'#e5e6cf');}}
  if(rac||has('tail')){const t=rac?'#9b8d91':skin;P([[16,46],[9,47],[4,43],[3,34],[5,28],[9,25],[14,27],[15,32],[12,38],[15,42],[19,42]],ink);P([[16,44],[9,45],[6,42],[5,35],[7,29],[9,27],[13,29],[13,32],[10,38],[13,43]],t);if(rac){R(5,33,7,4,'#51434f');R(7,28,6,3,'#51434f');R(8,41,6,3,'#51434f')}else{R(7,29,5,3,skL);R(7,35,3,2,skD)}}
  if(folk&&hd==='long'){P([[hl-2,headTop+3],[hl+6,headTop-4],[hr-5,headTop-4],[hr+3,headTop+5],[hr+4,38],[hr+1,45],[hr-4,44],[hr-7,40],[hl+5,43],[hl,46],[hl-5,40],[hl-4,26]],ink);P([[hl,headTop+4],[hl+7,headTop-2],[hr-6,headTop-2],[hr+1,headTop+5],[hr+2,37],[hr,43],[hr-4,42],[hr-7,38],[hl+4,41],[hl,43],[hl-3,38]],hair);P([[hl-1,24],[hl+2,23],[hl+2,36],[hl,40],[hl-2,36]],hM);P([[hr-3,23],[hr,27],[hr,40],[hr-3,39]],hD)}
  const footL=phase===1?2:0,footR=phase===-1?2:0,wide=(monster||alien)&&r.body==='round'?2:0;
  if(has('tentacles')&&alien){for(let i=0;i<4;i++){let x=12+i*7,off=i%2?footL:footR;P([[x,43],[x+5,43],[x+6,50],[x+4,55-off],[x-1,55-off],[x-2,52]],ink);R(x+1,45,3,6,skin);R(x,51-off,4,2,skD);R(x+1,49-off,2,1,skL)}}
  else if(!(alien||monster)||r.body!=='blob'){for(const [x,y] of [[16,footL],[26,footR]]){R(x,45,7,8-y,ink);R(x+1,46,5,6-y,has('goat')?'#876148':robot?skD:'#4c3c46');P([[x-2,51-y],[x+7,51-y],[x+9,54-y],[x+8,56-y],[x-2,56-y]],ink);R(x-1,52-y,7,2,has('goat')?'#866448':robot?skin:'#70523d');R(x,52-y,3,1,has('goat')?'#b4906c':gold);}}
  else{P([[9,44],[39,44],[40,50],[36,55],[30,54],[26,56],[21,54],[16,55],[10,53]],ink);P([[11,45],[37,45],[38,50],[35,53],[30,52],[26,54],[21,52],[16,53],[12,51]],skin);R(13,51,4,1,skL)}
  const top=Math.min(37,headBottom-1),bottom=r.body==='blob'&&!folk&&!rac&&!robot?51:49;
  // Tailored coat, readable lapels and cuffs instead of a plain colored bean.
  P([[16-wide,top-2],[32+wide,top-2],[38+wide,top+4],[38+wide,bottom-5],[35+wide,bottom-2],[33+wide,bottom-2],[34+wide,bottom+1],[14-wide,bottom+1],[15-wide,bottom-3],[10-wide,bottom-3],[10-wide,top+4]],ink);
  P([[17-wide,top],[31+wide,top],[36+wide,top+5],[36+wide,bottom-5],[32+wide,bottom-4],[32+wide,bottom-1],[16-wide,bottom-1],[16-wide,bottom-5],[12-wide,bottom-5],[12-wide,top+5]],coat);
  R(13-wide,top+5,3,bottom-top-8,coD);R(32+wide,top+5,3,bottom-top-8,coL);R(17-wide,bottom-3,15+wide*2,2,coD);
  if(!back){P([[19,top],[29,top],[27,top+7],[24,top+10],[20,top+5]],cream);P([[17,top],[21,top+1],[23,top+9],[19,top+6]],coD);P([[31,top],[27,top+1],[25,top+9],[29,top+6]],coD);R(23,top+7,2,Math.max(1,bottom-top-9),coD);for(let y=top+9;y<bottom-2;y+=4)dot(24,y);R(29,bottom-8,4,1,gold);R(15-wide,bottom-5,3,1,gold);R(31+wide,bottom-5,3,1,gold);if(r.outfit==='cardigan'){for(let x=18;x<=30;x+=3)R(x,bottom-6,1,3,coL)}}
  else{R(23,top+4,2,Math.max(1,bottom-top-6),coD);R(17,bottom-4,14,1,gold)}
  for(const x of [11-wide,34+wide]){R(x,bottom-7,3,1,gold);R(x,bottom-5,4,4,ink);R(x+1,bottom-4,2,2,rac?'#5d505a':robot?skD:skin)}
  // Neckwear is a separate feature, shared across all recipes.
  if(!back&&r.outfit==='bow'){P([[18,top],[23,top+2],[25,top+2],[30,top],[30,top+6],[25,top+4],[23,top+4],[18,top+6]],'#643b51');dot(23,top+2,shine)}
  if(r.outfit==='scarf'||r.shawl){R(17,top-1,14,4,ink);R(18,top,12,2,r.shawl?coL:'#a45955');if(!back){R(27,top+3,4,8,ink);R(28,top+3,2,7,'#ae6259');R(28,top+8,2,1,shine)}}
  if(!back&&r.pearls){for(let i=0;i<5;i++)R(19+i*2,top+2+(i===2?2:1),1,1,cream)}
  if(!back&&r.brooch)dot(30,top+5,shine);
  // Head silhouettes and unusual features. The exact recipe still belongs to the existing game.
  if(fae||has('ears')){for(const k of [-1,1]){P([[hx+k*9,cy-6],[hx+k*19,cy-10],[hx+k*17,cy],[hx+k*10,cy+4]],ink);P([[hx+k*10,cy-5],[hx+k*17,cy-8],[hx+k*15,cy],[hx+k*10,cy+2]],skin);R(hx+k*14-1,cy-3,2,2,skD)}}
  if(rac){for(const k of [-1,1]){B(hx+k*11-5,headTop-4,9,12,'#887a85');R(hx+k*11-2,headTop-1,4,5,'#c59399')}}
  if(robot){B(hl-3,cy-6,6,13,gold);B(hr-3,cy-6,6,13,gold);R(hx-1,headTop-5,2,6,ink);dot(hx-1,headTop-7,shine)}
  if(has('horns')||has('goat'))for(const k of [-1,1]){P([[hx+k*5,headTop+4],[hx+k*8,headTop-5],[hx+k*13,headTop-8],[hx+k*14,headTop-3],[hx+k*10,headTop+6]],ink);P([[hx+k*7,headTop+3],[hx+k*9,headTop-4],[hx+k*12,headTop-6],[hx+k*12,headTop-2],[hx+k*9,headTop+4]],'#ddbd8b');R(hx+k*10-1,headTop-1,2,1,'#977653')}
  if(has('antlers'))for(const k of [-1,1]){P([[hx+k*5,headTop+2],[hx+k*7,headTop-8],[hx+k*10,headTop-8],[hx+k*9,headTop-4],[hx+k*13,headTop-7],[hx+k*15,headTop-5],[hx+k*10,headTop-1],[hx+k*8,headTop+4]],'#81543f');leaf(hx+k*10,headTop-4,k)}
  if(has('antennae')&&alien){for(const k of r.eyes===1?[0]:[-1,1]){const x=hx+k*7;P([[x-1,headTop+1],[x-1+k*2,headTop-7],[x+1+k*3,headTop-7],[x+2,headTop+1]],ink);B(x+k*3-3,headTop-10,6,6,skL);dot(x+k*3-1,headTop-9,shine)}}
  const face=rac?'#a59ba0':robot?skin:skin,faceD=rac?'#71616b':skD,faceL=rac?'#d6c8c5':skL;
  B(hl,headTop,headW,headBottom-headTop,face);P([[hl+2,cy-3],[hl+4,cy+6],[hx-7,cy+10],[hx+7,cy+10],[hr-3,cy+5],[hr-2,cy+9],[hr-5,headBottom-1],[hl+5,headBottom-1],[hl+2,cy+7]],faceD);
  R(hl+5,headTop+3,8,2,faceL);R(hl+3,headTop+5,2,4,faceL);
  if(folk){if(hd==='bun'){B(hx-5,headTop-9,10,10,hair);R(hx-3,headTop-7,5,2,hM);R(hx-4,headTop-2,8,2,gold)}
    if(back){B(hl-1,headTop-2,headW+2,headBottom-headTop-2,hair);P([[hl+3,headTop+1],[hx-1,headTop-1],[hr-5,headTop+2],[hr-4,cy-3],[hx+1,cy-7],[hl+5,cy-5]],hM);R(hl+3,cy+1,2,5,hD);R(hr-5,cy,2,7,hD)}
    else{P([[hl-2,headTop+4],[hl+1,headTop-2],[hl+7,headTop-5],[hx+3,headTop-6],[hr-4,headTop-3],[hr+2,headTop+2],[hr+2,cy+2],[hr-2,cy+5],[hr-5,cy-5],[hx+4,cy-7],[hx-2,cy-3],[hx-9,cy-1],[hl+4,cy-4],[hl+3,cy+4],[hl-1,cy+2]],ink);
      P([[hl,headTop+4],[hl+3,headTop-1],[hl+8,headTop-3],[hx+3,headTop-4],[hr-5,headTop-1],[hr,headTop+3],[hr,cy+1],[hr-2,cy+2],[hr-4,cy-7],[hx+4,cy-9],[hx-2,cy-5],[hx-9,cy-3],[hl+3,cy-6],[hl+1,cy+1]],hair);
      P([[hl+3,headTop+3],[hl+8,headTop-1],[hx+2,headTop-3],[hr-6,headTop],[hx+1,headTop],[hx-5,headTop+5],[hl+4,headTop+6]],hM);R(hx-4,headTop-1,5,1,hL);P([[hl+2,headTop+6],[hl+4,headTop+4],[hl+4,cy-2],[hl+1,cy+2]],hD);
      if(hd==='curly')for(const [a,b] of [[hl-2,headTop+2],[hl+1,headTop-3],[hl+7,headTop-6],[hx+1,headTop-6],[hr-7,headTop-4],[hr-3,headTop],[hr-1,cy-6]]){B(a,b,7,7,hair);R(a+2,b+1,3,1,hM);R(a+1,b+3,1,2,hL)}}
  }else if(rac){P([[hx-6,headTop+1],[hx-4,headTop-4],[hx,headTop-1],[hx+3,headTop-5],[hx+8,headTop+1]],ink);P([[hx-5,headTop+1],[hx-3,headTop-2],[hx,headTop+1],[hx+3,headTop-3],[hx+6,headTop+1]],faceL);if(!back){P([[hl+2,cy-4],[hx-5,cy-7],[hx,cy-4],[hx+5,cy-7],[hr-2,cy-4],[hr-2,cy+3],[hx+5,cy+5],[hx,cy+1],[hx-5,cy+5],[hl+2,cy+3]],'#51434f');P([[hl+4,cy+5],[hx-4,cy+4],[hx,cy+2],[hx+4,cy+4],[hr-4,cy+5],[hx+7,cy+10],[hx-7,cy+10]],'#efe0ce');R(hx-2,cy+4,4,2,ink);R(hx-1,cy+4,1,1,'#dac9bf')}}
  else if(robot){if(!back){B(hl+3,cy-8,headW-6,16,'#273038');R(hl+6,cy-6,7,1,'#687477');R(hr-7,cy+4,3,1,'#687477');for(const k of [-1,1]){R(hx+k*6-2,cy-3,5,6,'#f1b85f');R(hx+k*6-1,cy-2,2,3,'#fff0ac')}R(hx-2,cy+5,4,1,shine)}else{R(hx-5,cy-3,10,1,faceD);R(hx-5,cy+1,10,1,faceD)}}
  else{if(has('fur'))for(let x=hl+3;x<hr-3;x+=5){P([[x-2,headTop+3],[x,headTop-3-(x%3)],[x+5,headTop+3]],ink);P([[x,headTop+2],[x,headTop-1-(x%3)],[x+3,headTop+2]],hair)}if(has('spots')){for(const [x,y] of [[hl+3,cy-3],[hr-5,cy-8],[hx-1,headTop+4],[hr-4,cy+4]])dot(x,y,skD)}}
  if(!back&&!robot){const col=r.iris||['#6f4a35','#4c7764','#695386','#376a88','#963e50'][seed%5],n=folk||rac?2:r.eyes||2,y=cy-3;
    if(n===1){eye(hx-4,y-2,9,10,col)}
    else{eye(hx-8,y,6,7,col);if(!side||dx>0)eye(hx+3,y,6,7,col);else eye(hx+3,y+1,4,6,col);if(n===3)eye(hx-2,y-7,5,6,col)}
    if(!rac){R(hx-1,cy+5,3,1,skD);R(hx-2,cy+8,4,1,ink);R(hx-1,cy+9,2,1,skD);if(r.tooth)R(hx+1,cy+8,2,2,cream);R(hx-10,cy+5,3,1,shade(skin,-.15));R(hx+8,cy+5,3,1,shade(skin,-.15));}
    else{R(hx-1,cy+7,3,1,ink);R(hx-6,cy+7,1,1,faceD);R(hx+6,cy+7,1,1,faceD)}
    if(r.specs){for(const x of [hx-9,hx+2]){R(x+1,y-2,8,1,gold);R(x,y-1,1,8,gold);R(x+9,y-1,1,8,gold);R(x+1,y+7,8,1,gold)}R(hx,y+1,3,1,gold)}}
  if(fae&&has('leaves')){for(let i=-2;i<=2;i++){leaf(hx+i*4,headTop+1+(i%2),i<0?-1:1)}flower(hx-7,headTop-1);flower(hx+5,headTop-2)}
  if(r.outfit==='hat'){P([[hx-13,headTop],[hx-10,headTop-3],[hx-9,headTop-10],[hx+7,headTop-10],[hx+10,headTop-3],[hx+13,headTop],[hx+13,headTop+3],[hx-13,headTop+3]],ink);R(hx-8,headTop-9,15,6,coD);R(hx-7,headTop-8,13,2,coat);R(hx-9,headTop-3,19,2,gold);R(hx-11,headTop,22,2,coat);dot(hx+5,headTop-4,shine)}
  if(carrying){P([[8,38],[39,38],[44,41],[44,44],[39,47],[8,47],[4,44],[4,41]],ink);P([[9,39],[38,39],[42,42],[39,45],[9,45],[6,42]],gold);R(13,40,21,3,cream);B(19,32,11,9,'#b9bfc1','#48424b');R(23,30,3,2,gold);R(21,34,5,1,'#f9ead1')}
}
