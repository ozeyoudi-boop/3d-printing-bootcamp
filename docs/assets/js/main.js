/* Auto-initialising course layer: progress, quizzes, copy buttons, theme, notes, design-for-print lab. */
(function(){
  var KEY='bootcamp3d:done', PAGES=['00-orientation','01-how-fdm-works','02-file-formats','03-design-first-model','04-design-for-print','05-edit-and-repair','06-slicing','07-x2d-and-materials','capstone'];
  function load(k,d){try{return JSON.parse(localStorage.getItem(k))||d}catch(e){return d}}
  function save(k,v){try{localStorage.setItem(k,JSON.stringify(v))}catch(e){}}
  var page=(location.pathname.split('/').pop()||'index.html').replace('.html','');
  var done=load(KEY,{});

  function paint(){
    var pct=Math.round(100*PAGES.filter(function(p){return done[p]}).length/PAGES.length);
    document.querySelectorAll('.bar i').forEach(function(i){i.style.width=pct+'%'});
    document.querySelectorAll('[data-pct]').forEach(function(e){e.textContent=pct+'%'});
    document.querySelectorAll('[data-st]').forEach(function(e){e.textContent=done[e.dataset.st]?'✓':''});
    var m=document.getElementById('mark');if(m)m.textContent=done[page]?'Completed ✓ (tap to undo)':'Mark module complete';
    var r=document.getElementById('resume');
    if(r){var next=PAGES.filter(function(p){return !done[p]})[0];r.href=(next||'reference')+'.html';r.textContent=next?(pct?'Resume course':'Start here'):'Review reference'}
  }
  var m=document.getElementById('mark');
  if(m)m.addEventListener('click',function(){done[page]=!done[page];save(KEY,done);paint()});

  var t=document.getElementById('theme');
  var th=load('bootcamp3d:theme','');if(th)document.documentElement.dataset.theme=th;
  if(t)t.addEventListener('click',function(){var n=document.documentElement.dataset.theme==='dark'?'light':'dark';document.documentElement.dataset.theme=n;save('bootcamp3d:theme',n)});

  document.querySelectorAll('pre').forEach(function(p){
    var b=document.createElement('button');b.className='copy';b.type='button';b.textContent='Copy';b.setAttribute('aria-label','Copy code');
    b.addEventListener('click',function(){var txt=p.querySelector('code')?p.querySelector('code').innerText:p.innerText;
      (navigator.clipboard?navigator.clipboard.writeText(txt):Promise.reject()).then(function(){b.textContent='Copied';setTimeout(function(){b.textContent='Copy'},1200)},function(){b.textContent='Select + copy'});});
    p.appendChild(b);
  });

  // quizzes: <div class="q" data-answer="1"><p>..</p><div class="opts"><button>..</button>..</div><div class="why">..</div></div>
  document.querySelectorAll('.quiz').forEach(function(quiz){
    var qs=quiz.querySelectorAll('.q'),score=quiz.querySelector('.score'),got=0,answered=0;
    qs.forEach(function(q){
      var ans=+q.dataset.answer;
      q.querySelectorAll('.opts button').forEach(function(b,i){
        b.addEventListener('click',function(){
          if(q.classList.contains('done'))return;
          q.classList.add('done');answered++;
          b.classList.add(i===ans?'right':'wrong');
          q.querySelectorAll('.opts button')[ans].classList.add('right');
          if(i===ans)got++;
          if(score)score.textContent='Score: '+got+' / '+qs.length+(answered===qs.length?(got>=Math.ceil(qs.length*0.7)?' — passed ✓':' — review and retry (reload page)'):'');
          if(answered===qs.length&&got>=Math.ceil(qs.length*0.7)){done[page]=true;save(KEY,done);paint()}
        });
      });
    });
  });

  var n=document.querySelector('textarea.notes');
  if(n){var nk='bootcamp3d:notes:'+page;n.value=load(nk,'');n.addEventListener('input',function(){save(nk,n.value)})}

  var lab=document.getElementById('dfp');
  if(lab){
    var g=function(id){return +lab.querySelector('#'+id).value};
    function run(){
      var wall=g('wall'),ang=g('ang'),hole=g('hole'),bridge=g('bridge'),gap=g('gap');
      lab.querySelectorAll('label').forEach(function(l){var o=l.querySelector('output'),i=l.querySelector('input');if(o&&i)o.textContent=i.value});
      var out=[];
      out.push(wall<1.2?['bad','Wall '+wall+' mm: thinner than 3 perimeters of a 0.4 mm nozzle — weak or skipped. Use ≥1.2 mm (≥2.0 mm for load-bearing).']:wall<2?['warn','Wall '+wall+' mm: fine for light parts; go ≥2 mm for anything that carries load.']:['ok','Wall '+wall+' mm: solid.']);
      out.push(ang>60?['bad','Overhang '+ang+'° from vertical: needs support or a redesign (chamfer to 45°).']:ang>45?['warn','Overhang '+ang+'°: prints with a rough underside; chamfer to ≤45° if the surface matters.']:['ok','Overhang '+ang+'°: prints clean without support.']);
      out.push(hole<3?['warn','Hole '+hole+' mm: small holes shrink; drill/ream after printing or add 0.2–0.3 mm.']:['ok','Hole '+hole+' mm: fine to print. Remember the CAD size should be your target diameter +0.2–0.4 mm.']);
      out.push(bridge>50?['bad','Bridge '+bridge+' mm: will sag. Add a support or an arch.']:bridge>25?['warn','Bridge '+bridge+' mm: ok with tuned bridging, expect some droop.']:['ok','Bridge '+bridge+' mm: bridges well.']);
      out.push(gap<0.1?['bad','Moving-part gap '+gap+' mm: parts will fuse. Use ≥0.2 mm for a snug slide, 0.3–0.4 for loose.']:gap<0.2?['warn','Gap '+gap+' mm: tight press/snug fit; test a calibration print first.']:['ok','Gap '+gap+' mm: sliding clearance is realistic.']);
      lab.querySelector('#dfp-out').innerHTML=out.map(function(o){return '<p class="verdict '+o[0]+'">'+o[1]+'</p>'}).join('');
    }
    lab.addEventListener('input',run);run();
  }
  paint();
})();
