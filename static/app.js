const samples = [
'Machine learning algorithms identify patterns in training data and improve predictions.',
'Artificial intelligence systems use neural networks for image recognition and language processing.',
'Data scientists build machine learning models and evaluate prediction accuracy.',
'Football players train daily and score goals during championship matches.',
'Basketball teams practice shooting passing and defending to win games.',
'Cricket players compete in tournaments with bowlers and batsmen.',
'Doctors diagnose patients and provide treatment in modern hospitals.',
'Medical researchers investigate diseases and develop healthcare treatments.',
'Hospitals employ nurses and doctors to deliver patient care and medicine.',
'Astronomers study distant galaxies and observe stars with telescopes.',
'Space missions send spacecraft to explore planets and distant moons.',
'Telescopes collect light from galaxies and reveal new stars and planets.'
];
const $ = id => document.getElementById(id);
function reset(){ $('documents').value=samples.join('\n'); $('topicSlider').value=4; $('topicCount').textContent='4'; $('error').textContent=''; }
$('sampleBtn').addEventListener('click',reset);
$('topicSlider').addEventListener('input',e=>$('topicCount').textContent=e.target.value);
function elem(tag, className, text){const e=document.createElement(tag);if(className)e.className=className;if(text!==undefined)e.textContent=text;return e;}
function render(data){ $('metricDocs').textContent=data.documents;$('metricTopics').textContent=data.topics.length;$('metricVocab').textContent=data.vocabulary;$('metricTokens').textContent=data.tokens;
 const cards=$('topicCards');cards.replaceChildren();
 data.topics.forEach(topic=>{const card=elem('article','topic-card');const head=elem('div','topic-top');head.append(elem('h4','',`Topic ${String(topic.id).padStart(2,'0')}`),elem('span','topic-badge',`${topic.token_count} TOKENS`));card.append(head);
 const maximum=Math.max(...topic.words.map(w=>w.probability),0.00001);
 topic.words.forEach(w=>{const line=elem('div','word-line');const meta=elem('div','word-meta');meta.append(elem('span','',w.word),elem('span','',`${(w.probability*100).toFixed(1)}%`));const track=elem('div','track');const fill=elem('div','fill');fill.style.width=`${100*w.probability/maximum}%`;track.append(fill);line.append(meta,track);card.append(line);});cards.append(card);});
 const rows=$('documentRows');rows.replaceChildren();data.classifications.forEach((doc,i)=>{const tr=elem('tr');tr.append(elem('td','',`${i+1}. ${doc.document}`));const topic=elem('td');topic.append(elem('span','pill',`Topic ${String(doc.topic).padStart(2,'0')}`));tr.append(topic,elem('td','',`${(doc.probability*100).toFixed(1)}%`));rows.append(tr);});$('results').hidden=false;$('results').scrollIntoView({behavior:'smooth',block:'start'});
}
$('analyzeBtn').addEventListener('click',async()=>{const documents=$('documents').value.split(/\r?\n/).map(s=>s.trim()).filter(Boolean);const topics=Number($('topicSlider').value);$('error').textContent='';if(documents.length<3){$('error').textContent='Enter at least three nonempty documents.';return;}if(topics>documents.length){$('error').textContent='Number of topics cannot exceed number of documents.';return;}const btn=$('analyzeBtn');btn.disabled=true;btn.textContent='Analyzing your corpus…';try{const response=await fetch('/api/analyze',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({documents,topics})});const result=await response.json();if(!response.ok)throw Error(result.error||'Analysis failed');render(result);}catch(error){$('error').textContent=error.message;}finally{btn.disabled=false;btn.innerHTML='✦ &nbsp; Run topic discovery <span>→</span>';}});
reset();
