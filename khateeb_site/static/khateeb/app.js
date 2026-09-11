const langs = window.LANGUAGES || {};
const UI = {
  ar:{brand:'الخطيب المترجم',home:'مرحبًا بك في',hero:'ترجمة نصية فورية تساعدك على فهم الخطبة بلغتك، بهدوء وبدون أي صوت يصدر من الموقع.',choose:'اختر لغتك',step1:'الخطوة 1',chooseTitle:'اختر لغتك',chooseHint:'اختر اللغة التي تريد أن تظهر بها الترجمة.',search:'ابحث عن لغة...',notice:'تنبيه مهم',brother:'أخي المسلم',hadithIntro:'تذكّر حديث رسول الله ﷺ:',hadithGrade:'خلاصة حكم المحدث: صحيح',noticeText:'استخدم الموقع فقط لمساعدتك على فهم كلام الخطيب، ولا تنشغل بالجوال أثناء الخطبة. لا يصدر الموقع أي صوت.',understand:'أفهم ذلك — بدء الترجمة',step2:'الخطوة 2',live:'الترجمة المباشرة',ready:'جاهز',listen:'بدء الاستماع',stop:'إيقاف الاستماع',noSound:'لن يصدر الموقع أي صوت',clear:'مسح النص',font:'تكبير النص',smallFont:'تصغير النص',change:'تغيير اللغة',warning:'الترجمة آلية وقد تحتوي على أخطاء؛ الهدف هو المساعدة على الفهم.',micError:'تعذر الوصول إلى الميكروفون. اسمح للموقع باستخدامه ثم حاول مرة أخرى.',browserError:'التعرف المباشر على الكلام غير مدعوم في هذا المتصفح. جرّب Google Chrome أو Microsoft Edge.',apiError:'تعذرت الترجمة الآن. تأكد من إعداد OPENAI_API_KEY على الخادم.',footer:'خدمة نصية لمساعدة المصلين على فهم الخطبة بلغاتهم.',rights:'جميع الحقوق محفوظة لأسرة الصناديد® 2026'},
  en:{brand:'Al-Khateeb Translator',home:'Welcome to',hero:'Live text translation to help you understand the Friday sermon in your language, quietly and without any sound from the website.',choose:'Choose your language',step1:'Step 1',chooseTitle:'Choose your language',chooseHint:'Choose the language you want the translation to appear in.',search:'Search for a language...',notice:'Important notice',brother:'Dear Muslim',hadithIntro:'Remember the saying of the Prophet ﷺ:',hadithGrade:'Hadith grading: Authentic',noticeText:'Use this website only to help you understand the sermon. Do not become distracted by your phone during the sermon. The website produces no sound.',understand:'I understand — Start translation',step2:'Step 2',live:'Live translation',ready:'Ready',listen:'Start listening',stop:'Stop listening',noSound:'The website produces no sound',clear:'Clear text',font:'Increase text',smallFont:'Decrease text',change:'Change language',warning:'Machine translation may contain errors; it is intended to assist understanding.',micError:'Microphone access failed. Allow microphone access and try again.',browserError:'Live speech recognition is not supported in this browser. Try Google Chrome or Microsoft Edge.',apiError:'Translation failed. Make sure OPENAI_API_KEY is configured on the server.',footer:'A text service to help worshippers understand the sermon in their languages.',rights:'All rights reserved to Al-Sanadid Family® 2026'}
};
let chosen='ar', uiLang='ar', rec=null, running=false, started=0, timer=null, fontBig=false;
const $ = id => document.getElementById(id);
const rtlCodes = new Set(['ar','ur','fa','ps','sd','ku']);
function go(id){ ['home','langs','notice','live'].forEach(x=>{const el=$(x); if(el) el.classList.toggle('hidden',x!==id);}); window.scrollTo({top:0,behavior:'smooth'}); }
function t(){return UI[uiLang] || UI.ar;}
function setText(id,value){const el=$(id);if(el)el.textContent=value;}
function applyUI(){
  const x=t(); document.documentElement.lang=uiLang; document.documentElement.dir=rtlCodes.has(uiLang)?'rtl':'ltr';
  setText('brandText',x.brand); setText('start',x.choose+'  ←'); setText('heroTitle',x.home); setText('heroBrand',x.brand); setText('heroDesc',x.hero); setText('heroNote','🔇 '+(uiLang==='ar'?'نص فقط • 📱 مصمم للجوال':'Text only • 📱 Mobile friendly'));
  setText('step1',x.step1);setText('chooseTitle',x.chooseTitle);setText('chooseHint',x.chooseHint); $('search').placeholder=x.search;
  setText('noticeEyebrow',x.notice);setText('noticeTitle',x.brother);setText('hadithIntro',x.hadithIntro);setText('hadithGrade',x.hadithGrade);setText('noticeText',x.noticeText);setText('goLive',x.understand);
  setText('step2',x.step2); setText('langTitle',(langs[chosen]||chosen)+' — '+x.live); setText('langName',langs[chosen]||chosen); setText('micText',running?x.stop:x.listen); setText('micNote',x.noSound); setText('clear',x.clear); setText('font',fontBig?x.smallFont:x.font); setText('change',x.change); setText('warning',x.warning); setText('status',running?'● '+x.stop:x.ready); setText('footerDesc',x.footer);setText('rights',x.rights); setText('homeLang',uiLang==='ar'?'English':'العربية');
}
function render(q=''){
  const query=q.trim().toLowerCase(); const entries=Object.entries(langs).filter(([c,n])=>(n+' '+c).toLowerCase().includes(query));
  $('grid').innerHTML=entries.map(([c,n])=>`<button type="button" class="lang ${c==='ar'?'ar':''}" data-c="${c}">${n}<small>${c}</small></button>`).join('');
  $('grid').querySelectorAll('.lang').forEach(b=>b.addEventListener('click',()=>{chosen=b.dataset.c;uiLang=(chosen==='ar'?'ar':'en');setText('langName',langs[chosen]);$('out').textContent='';$('out').dataset.empty='yes';$('interim').textContent='';applyUI();go('notice');}));
}
function clock(){clearInterval(timer);timer=setInterval(()=>{const s=Math.floor((Date.now()-started)/1000);setText('timer',`${String(Math.floor(s/60)).padStart(2,'0')}:${String(s%60).padStart(2,'0')}`)},500)}
function stopClock(){clearInterval(timer);timer=null;setText('timer','00:00')}
function add(text){if(!text)return;if($('out').dataset.empty!=='no'){$('out').textContent='';$('out').dataset.empty='no'}$('out').textContent+=($('out').textContent?' ':'')+text}
async function translate(text){
  if(!text)return;
  if(chosen==='ar'){add(text);return;}
  try{
    const r=await fetch('/api/translate/',{method:'POST',headers:{'Content-Type':'application/json','X-Requested-With':'XMLHttpRequest'},body:JSON.stringify({text,target:chosen})});
    let data={};try{data=await r.json()}catch(e){}
    if(!r.ok || !data.text) throw new Error(data.error || t().apiError);
    add(data.text);
  }catch(e){console.error(e);setText('status',e.message||t().apiError);}
}
function makeRec(){
  const SR=window.SpeechRecognition||window.webkitSpeechRecognition;if(!SR)return null;
  const r=new SR();r.lang='ar-SA';r.continuous=true;r.interimResults=true;r.maxAlternatives=1;
  r.onresult=e=>{let interim='';for(let i=e.resultIndex;i<e.results.length;i++){const text=e.results[i][0].transcript;if(e.results[i].isFinal)translate(text.trim());else interim+=text;}$('interim').textContent=interim;};
  r.onerror=e=>{console.error(e);if(e.error==='not-allowed'||e.error==='service-not-allowed')setText('status',t().micError);else if(e.error!=='aborted')setText('status',t().browserError);};
  r.onend=()=>{if(running){try{r.start()}catch(e){}}};return r;
}
function toggleUI(){uiLang=uiLang==='ar'?'en':'ar';applyUI();render($('search').value);}
$('start').onclick=()=>go('langs');
$('homeLang').onclick=toggleUI;
$('search').oninput=e=>render(e.target.value);
$('goLive').onclick=()=>go('live');
$('change').onclick=()=>go('langs');
$('clear').onclick=()=>{$('out').textContent='';$('out').dataset.empty='yes';$('interim').textContent=''};
$('font').onclick=()=>{fontBig=!fontBig;$('out').style.fontSize=fontBig?'30px':'22px';applyUI()};
$('mic').onclick=async()=>{
  if(running){running=false;try{rec&&rec.stop()}catch(e){}$('mic').classList.remove('on');applyUI();stopClock();return;}
  if(!navigator.mediaDevices?.getUserMedia){alert(t().micError);return;}
  try{const stream=await navigator.mediaDevices.getUserMedia({audio:true});stream.getTracks().forEach(track=>track.stop());}catch(e){alert(t().micError);return;}
  rec=makeRec();if(!rec){alert(t().browserError);return;}
  running=true;$('out').textContent='';$('out').dataset.empty='yes';$('interim').textContent='';$('mic').classList.add('on');started=Date.now();clock();applyUI();try{rec.start()}catch(e){setText('status',t().browserError)}
};
render();applyUI();
